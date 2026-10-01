from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import Skill, Goal, PracticeSession, Post

router=APIRouter(prefix="/api/analytics",tags=["Analytics"])

@router.get("/overview")
def overview(user=Depends(get_current_user),db:Session=Depends(get_db)):
    skills=db.query(func.count(Skill.id)).filter(Skill.user_id==user.id).scalar()
    goals=db.query(func.count(Goal.id)).filter(Goal.user_id==user.id).scalar()
    posts=db.query(func.count(Post.id)).filter(Post.user_id==user.id).scalar()
    minutes=db.query(func.coalesce(func.sum(PracticeSession.duration_minutes),0)).filter(PracticeSession.user_id==user.id).scalar()
    active=db.query(func.count(Goal.id)).filter(Goal.user_id==user.id,Goal.status=="active").scalar()
    return {"skills":skills,"goals":goals,"active_goals":active,"posts":posts,
            "practice_minutes":int(minutes or 0),"practice_hours":round((minutes or 0)/60,2)}
