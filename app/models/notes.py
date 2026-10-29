from typing import Optional
from pydantic import BaseModel

class DecisionNote(BaseModel):
    id: Optional[int] = None
    task_id: int
    note_title: str
    note_body: str
    decision_flag: bool
    created_at: Optional[str] = None