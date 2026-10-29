from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.founder_task import FounderTaskHistoryItem, FounderTaskInput
from app.models.notes import DecisionNote
from app.models.founder_task import DecisionNoteInput
from app.services.export_service import ExportService
from app.services.notes_service import NotesService
from app.services.task_repository import TaskRepository
from app.services.task_runner import TaskRunner

router = APIRouter(prefix="/api/v1", tags=["founder-agent"])

task_runner = TaskRunner()
task_repository = TaskRepository()
notes_service = NotesService()
export_service = ExportService()

@router.get("/health")
async def health_check():
    return {
        "status": "ok",
        "service": "FounderFlow",
        "gemini_configured": task_runner.gemini.is_ready(),
    }

@router.post("/task")
async def run_founder_task(task: FounderTaskInput, db: Session = Depends(get_db)):
    try:
        result = await task_runner.run_task(task)
        saved_record = task_repository.save_task(db, task.model_dump(), result)
        response = saved_record.to_public_dict()

        return {
            "id": response["id"],
            "task_type": response["task_type"],
            "company_name": response["company_name"],
            "summary": response["summary"],
            "findings": response["findings"],
            "recommended_next_steps": response["recommended_next_steps"],
            "confidence": response["confidence"],
            "human_judgment_required": response["human_judgment_required"],
            "created_at": response["created_at"],
            "workflow": result.get("workflow"),
            "lead_generation": result.get("lead_generation"),
        }
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc))

@router.get("/history", response_model=List[FounderTaskHistoryItem])
async def get_task_history(db: Session = Depends(get_db)):
    records = task_repository.list_recent(db, limit=10)
    return [
        FounderTaskHistoryItem(
            id=record.id,
            task_type=record.task_type,
            company_name=record.company_name,
            created_at=record.created_at.isoformat(),
            summary=record.summary[:180],
        )
        for record in records
    ]

@router.post("/notes", response_model=DecisionNote)
async def create_note(note: DecisionNoteInput, db: Session = Depends(get_db)):
    task = task_repository.get_by_id(db, note.task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    saved = notes_service.add_note(
        db,
        note.task_id,
        note.note_title,
        note.note_body,
        note.decision_flag,
    )

    return DecisionNote(
        id=saved.id,
        task_id=saved.task_id,
        note_title=saved.note_title,
        note_body=saved.note_body,
        decision_flag=saved.decision_flag,
        created_at=saved.created_at.isoformat(),
    )

@router.get("/notes/{task_id}", response_model=List[DecisionNote])
async def get_notes(task_id: int, db: Session = Depends(get_db)):
    task = task_repository.get_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    notes = notes_service.list_notes(db, task_id)
    return [
        DecisionNote(
            id=n.id,
            task_id=n.task_id,
            note_title=n.note_title,
            note_body=n.note_body,
            decision_flag=n.decision_flag,
            created_at=n.created_at.isoformat(),
        )
        for n in notes
    ]

@router.get("/export/{task_id}")
async def export_task(task_id: int, db: Session = Depends(get_db)):
    task = task_repository.get_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    summary = export_service.build_summary(task.to_public_dict())
    content = export_service.render_txt(summary)

    return {
        "task_id": task_id,
        "content": content,
        "filename": f"founderflow_{task_id}_summary.txt",
        "mime_type": "text/plain",
    }