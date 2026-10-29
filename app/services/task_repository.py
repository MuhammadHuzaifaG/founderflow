from typing import List, Optional
from sqlalchemy.orm import Session

from app.db import FounderTaskRecord

class TaskRepository:
    def save_task(self, db: Session, task_data: dict, result: dict) -> FounderTaskRecord:
        record = FounderTaskRecord(
            task_type=task_data["task_type"],
            company_name=task_data["company_name"],
            market=task_data["market"],
            founder_goal=task_data["founder_goal"],
            context=task_data.get("context"),
            summary=result["summary"],
            findings=result["findings"],
            recommended_next_steps=result["recommended_next_steps"],
            confidence=result["confidence"],
            human_judgment_required=result.get("human_judgment_required", True),
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        return record

    def list_recent(self, db: Session, limit: int = 10) -> List[FounderTaskRecord]:
        return (
            db.query(FounderTaskRecord)
            .order_by(FounderTaskRecord.created_at.desc())
            .limit(limit)
            .all()
        )

    def get_by_id(self, db: Session, task_id: int) -> Optional[FounderTaskRecord]:
        return db.query(FounderTaskRecord).filter(FounderTaskRecord.id == task_id).first()