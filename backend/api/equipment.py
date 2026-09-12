from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from models.database import get_db
from models.equipment import EquipmentProfile

router = APIRouter(prefix="/api/equipment", tags=["equipment"])


class EquipmentIn(BaseModel):
    category: str
    manufacturer: str | None = None
    model: str | None = None
    function: str | None = None
    notes: str = ""


class EquipmentOut(EquipmentIn):
    id: str

    model_config = ConfigDict(from_attributes=True)


@router.post("", response_model=EquipmentOut, status_code=201)
def create_profile(payload: EquipmentIn, db: Session = Depends(get_db)):
    """
    Proof-of-concept for the vendor-neutral principle: adding a new piece of
    equipment is a data write here, never a code change in rules/dsng_tree.py.
    """
    profile = EquipmentProfile(**payload.model_dump())
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


@router.get("", response_model=list[EquipmentOut])
def list_profiles(category: str | None = None, db: Session = Depends(get_db)):
    q = db.query(EquipmentProfile)
    if category:
        q = q.filter(EquipmentProfile.category == category)
    return q.all()


@router.get("/{profile_id}", response_model=EquipmentOut)
def get_profile(profile_id: str, db: Session = Depends(get_db)):
    profile = db.get(EquipmentProfile, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Equipment profile not found")
    return profile
