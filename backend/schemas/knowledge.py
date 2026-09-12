from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, field_validator


class KnowledgeCreate(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    category: str = "other"
    causes: str = Field(min_length=3)
    fix: str = Field(min_length=3)
    notes: str = ""
    author: str = "Unspecified engineer"

    @field_validator("title", "causes", "fix")
    @classmethod
    def not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("must not be blank")
        return v.strip()


class KnowledgeOut(BaseModel):
    id: str
    title: str
    category: str
    causes: str
    fix: str
    notes: str
    author: str
    validation_state: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ReviewDecision(BaseModel):
    decision: str  # "approved" | "rejected"

    @field_validator("decision")
    @classmethod
    def valid_decision(cls, v: str) -> str:
        if v not in ("approved", "rejected"):
            raise ValueError("decision must be 'approved' or 'rejected'")
        return v
