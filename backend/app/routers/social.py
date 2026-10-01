from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User, Follow

router=APIRouter(prefix="/api/users",tags=["Social"])

@router.post("/{user_id}/follow")
def toggle_follow(user_id:int,user=Depends(get_current_user),db:Session=Depends(get_db)):
    if user_id==user.id: raise HTTPException(400,"Cannot follow yourself")
    if not db.get(User,user_id): raise HTTPException(404,"User not found")
    f=db.query(Follow).filter(Follow.follower_id==user.id,Follow.following_id==user_id).first()
    if f: db.delete(f); following=False
    else: db.add(Follow(follower_id=user.id,following_id=user_id)); following=True
    db.commit(); return {"following":following}
