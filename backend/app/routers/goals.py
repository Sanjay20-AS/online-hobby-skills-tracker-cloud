from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import Goal, Milestone
from app.schemas.domain import GoalCreate, GoalOut, MilestoneCreate, MilestoneOut

router = APIRouter(prefix="/api", tags=["Goals"])

@router.get("/goals", response_model=list[GoalOut])
def list_goals(user=Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Goal).filter(Goal.user_id == user.id).all()

@router.post("/goals", response_model=GoalOut)
def create_goal(data: GoalCreate, user=Depends(get_current_user), db: Session = Depends(get_db)):
    item=Goal(user_id=user.id, **data.model_dump()); db.add(item); db.commit(); db.refresh(item); return item

@router.put("/goals/{goal_id}", response_model=GoalOut)
def update_goal(goal_id:int, data:GoalCreate, user=Depends(get_current_user), db:Session=Depends(get_db)):
    item=db.query(Goal).filter(Goal.id==goal_id, Goal.user_id==user.id).first()
    if not item: raise HTTPException(404,"Goal not found")
    for k,v in data.model_dump().items(): setattr(item,k,v)
    db.commit(); db.refresh(item); return item

@router.delete("/goals/{goal_id}")
def delete_goal(goal_id:int,user=Depends(get_current_user),db:Session=Depends(get_db)):
    item=db.query(Goal).filter(Goal.id==goal_id,Goal.user_id==user.id).first()
    if not item: raise HTTPException(404,"Goal not found")
    db.delete(item); db.commit(); return {"message":"Goal deleted"}

@router.get("/goals/{goal_id}/milestones",response_model=list[MilestoneOut])
def milestones(goal_id:int,user=Depends(get_current_user),db:Session=Depends(get_db)):
    goal=db.query(Goal).filter(Goal.id==goal_id,Goal.user_id==user.id).first()
    if not goal: raise HTTPException(404,"Goal not found")
    return db.query(Milestone).filter(Milestone.goal_id==goal_id).all()

@router.post("/goals/{goal_id}/milestones",response_model=MilestoneOut)
def create_milestone(goal_id:int,data:MilestoneCreate,user=Depends(get_current_user),db:Session=Depends(get_db)):
    goal=db.query(Goal).filter(Goal.id==goal_id,Goal.user_id==user.id).first()
    if not goal: raise HTTPException(404,"Goal not found")
    item=Milestone(goal_id=goal_id,**data.model_dump()); db.add(item); db.commit(); db.refresh(item); return item

@router.put("/milestones/{milestone_id}")
def toggle_milestone(milestone_id:int,user=Depends(get_current_user),db:Session=Depends(get_db)):
    item=db.query(Milestone).join(Goal).filter(Milestone.id==milestone_id,Goal.user_id==user.id).first()
    if not item: raise HTTPException(404,"Milestone not found")
    item.completed=not item.completed; db.commit(); return {"completed":item.completed}
