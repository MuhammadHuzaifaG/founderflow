from typing import List
from sqlalchemy.orm import Session

from app.db import DecisionNoteRecord

class NotesService:
    def add_note(self, db: Session, task_id: int, note_title: str, note_body: str, decision_flag: bool = False) -> DecisionNoteRecord:
        record = DecisionNoteRecord(
            task_id=task_id,
            note_title=note_title,
            note_body=note_body,
            decision_flag=decision_flag,
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        return record

    def list_notes(self, db: Session, task_id: int) -> List[DecisionNoteRecord]:
        return (
            db.query(DecisionNoteRecord)
            .filter(DecisionNoteRecord.task_id == task_id)
            .order_by(DecisionNoteRecord.created_at.desc())
            .all()
        )