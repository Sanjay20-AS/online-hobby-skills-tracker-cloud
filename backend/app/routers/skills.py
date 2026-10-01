from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import Skill
from app.schemas.domain import SkillCreate, SkillOut

router = APIRouter(prefix="/api/skills", tags=["Skills"])

@router.get("", response_model=list[SkillOut])
def list_skills(user=Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Skill).filter(Skill.user_id == user.id).all()

@router.post("", response_model=SkillOut)
def create_skill(data: SkillCreate, user=Depends(get_current_user), db: Session = Depends(get_db)):
    item = Skill(user_id=user.id, **data.model_dump())
    db.add(item); db.commit(); db.refresh(item)
    return item

@router.put("/{skill_id}", response_model=SkillOut)
def update_skill(skill_id: int, data: SkillCreate, user=Depends(get_current_user), db: Session = Depends(get_db)):
    item = db.query(Skill).filter(Skill.id == skill_id, Skill.user_id == user.id).first()
    if not item: raise HTTPException(404, "Skill not found")
    for k,v in data.model_dump().items(): setattr(item,k,v)
    db.commit(); db.refresh(item); return item

@router.delete("/{skill_id}")
def delete_skill(skill_id: int, user=Depends(get_current_user), db: Session = Depends(get_db)):
    item = db.query(Skill).filter(Skill.id == skill_id, Skill.user_id == user.id).first()
    if not item: raise HTTPException(404, "Skill not found")
    db.delete(item); db.commit(); return {"message": "Skill deleted"}
