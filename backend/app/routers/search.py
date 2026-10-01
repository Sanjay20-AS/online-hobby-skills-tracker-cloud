from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User, Skill

router=APIRouter(prefix="/api/search",tags=["Search"])

@router.get("")
def search(q:str=Query(min_length=1),user=Depends(get_current_user),db:Session=Depends(get_db)):
    pattern=f"%{q}%"
    users=db.query(User).filter(or_(User.username.ilike(pattern),User.email.ilike(pattern))).limit(10).all()
    skills=db.query(Skill).filter(Skill.name.ilike(pattern)).limit(10).all()
    return {"users":[{"type":"user","id":x.id,"label":x.username} for x in users],
            "skills":[{"type":"skill","id":x.id,"label":x.name} for x in skills]}
