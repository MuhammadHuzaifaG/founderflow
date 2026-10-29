from typing import Literal, Optional
from pydantic import BaseModel, Field

class FounderTaskInput(BaseModel):
    task_type: Literal[
        "market_scan",
        "lead_generation",
        "customer_discovery",
        "competitive_analysis",
        "meeting_summary",
        "investor_prep",
    ]
    company_name: str = Field(..., min_length=2, max_length=120)
    market: str = Field(..., min_length=2, max_length=200)
    founder_goal: str = Field(..., min_length=20, max_length=4000)
    context: Optional[str] = Field(default=None, max_length=8000)
    output_length: int = Field(default=700, ge=150, le=2000)

class FounderTaskHistoryItem(BaseModel):
    id: int
    task_type: str
    company_name: str
    created_at: str
    summary: str

class DecisionNoteInput(BaseModel):
    task_id: int
    note_title: str = Field(..., min_length=2, max_length=120)
    note_body: str = Field(..., min_length=10, max_length=4000)
    decision_flag: bool = False