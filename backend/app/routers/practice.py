from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import PracticeSession
from app.schemas.domain import PracticeCreate, PracticeOut

router=APIRouter(prefix="/api/practice",tags=["Practice"])

@router.get("",response_model=list[PracticeOut])
def list_practice(user=Depends(get_current_user),db:Session=Depends(get_db)):
    return db.query(PracticeSession).filter(PracticeSession.user_id==user.id).order_by(PracticeSession.id.desc()).all()

@router.post("",response_model=PracticeOut)
def create_practice(data:PracticeCreate,user=Depends(get_current_user),db:Session=Depends(get_db)):
    item=PracticeSession(user_id=user.id,**data.model_dump()); db.add(item); db.commit(); db.refresh(item); return item

@router.get("/analytics")
def practice_analytics(user=Depends(get_current_user),db:Session=Depends(get_db)):
    total=db.query(func.coalesce(func.sum(PracticeSession.duration_minutes),0)).filter(PracticeSession.user_id==user.id).scalar()
    count=db.query(func.count(PracticeSession.id)).filter(PracticeSession.user_id==user.id).scalar()
    return {"total_minutes":int(total or 0),"total_hours":round((total or 0)/60,2),"sessions":count}
