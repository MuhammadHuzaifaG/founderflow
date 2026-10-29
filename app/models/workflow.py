from typing import List
from pydantic import BaseModel

class DecisionCheckpoint(BaseModel):
    stage: str
    question: str
    rationale: str
    owner: str = "Founder"

class WorkflowStep(BaseModel):
    name: str
    goal: str
    input_needed: List[str]
    output_expected: str

class FounderWorkflow(BaseModel):
    workflow_name: str
    summary: str
    steps: List[WorkflowStep]
    decision_checkpoints: List[DecisionCheckpoint]
    validation_summary: str