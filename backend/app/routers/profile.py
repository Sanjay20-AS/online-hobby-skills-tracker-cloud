from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import Profile
from app.schemas.domain import ProfileUpdate

router = APIRouter(prefix="/api/profile", tags=["Profile"])

@router.get("")
def get_profile(user=Depends(get_current_user), db: Session = Depends(get_db)):
    p = db.query(Profile).filter(Profile.user_id == user.id).first()
    return {"user": {"id": user.id, "email": user.email, "username": user.username},
            "profile": {"full_name": p.full_name, "bio": p.bio, "avatar_url": p.avatar_url}}

@router.put("")
def update_profile(data: ProfileUpdate, user=Depends(get_current_user), db: Session = Depends(get_db)):
    p = db.query(Profile).filter(Profile.user_id == user.id).first()
    p.full_name, p.bio = data.full_name, data.bio
    db.commit()
    return {"message": "Profile updated"}
