from typing import List, Optional
from pydantic import BaseModel

class ExportSummary(BaseModel):
    company_name: str
    task_type: str
    summary: str
    findings: List[str]
    next_steps: List[str]
    confidence: float
    created_at: Optional[str] = None