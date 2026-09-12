from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import desc
from sqlalchemy.orm import Session

from models.database import get_db
from models.knowledge import KnowledgeEntry
from schemas.knowledge import KnowledgeCreate, KnowledgeOut, ReviewDecision

router = APIRouter(prefix="/api/knowledge", tags=["knowledge"])


@router.post("", response_model=KnowledgeOut, status_code=201)
def create_entry(payload: KnowledgeCreate, db: Session = Depends(get_db)):
    """
    Log a field-discovered fault/fix. Always created as validation_state
    'pending' -- per the controlled-learning principle, nothing here is
    promoted to verified departmental knowledge without a human review
    (see /review below), even though it is immediately visible to the team.
    """
    entry = KnowledgeEntry(**payload.model_dump())
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


@router.get("", response_model=list[KnowledgeOut])
def list_entries(category: str | None = None, db: Session = Depends(get_db)):
    q = db.query(KnowledgeEntry).order_by(desc(KnowledgeEntry.created_at))
    if category:
        q = q.filter(KnowledgeEntry.category == category)
    return q.all()


@router.get("/{entry_id}", response_model=KnowledgeOut)
def get_entry(entry_id: str, db: Session = Depends(get_db)):
    entry = db.get(KnowledgeEntry, entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Knowledge entry not found")
    return entry


@router.delete("/{entry_id}", status_code=204)
def delete_entry(entry_id: str, db: Session = Depends(get_db)):
    entry = db.get(KnowledgeEntry, entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Knowledge entry not found")
    db.delete(entry)
    db.commit()


@router.post("/{entry_id}/review", response_model=KnowledgeOut)
def review_entry(entry_id: str, decision: ReviewDecision, db: Session = Depends(get_db)):
    """
    Phase 3 stub: a reviewer approves or rejects a contribution. There is no
    auth/reviewer-identity model yet (see ARCHITECTURE.md, Phase 3/4) -- this
    endpoint exists so the frontend and future auth layer have a stable
    contract to build against, not to represent a finished workflow.
    """
    entry = db.get(KnowledgeEntry, entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Knowledge entry not found")
    entry.validation_state = decision.decision
    db.commit()
    db.refresh(entry)
    return entry
