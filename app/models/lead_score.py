from typing import List
from pydantic import BaseModel, Field

class LeadOpportunity(BaseModel):
    name: str
    segment: str
    urgency: int = Field(ge=1, le=10)
    fit: int = Field(ge=1, le=10)
    access: int = Field(ge=1, le=10)
    score: int = Field(ge=1, le=100)
    reason: str
    next_step: str

class LeadGenerationResult(BaseModel):
    summary: str
    opportunity_cards: List[LeadOpportunity]
    founder_decision_prompt: str