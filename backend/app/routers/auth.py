from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import hash_password, verify_password, create_token, get_current_user
from app.models.user import User, Profile
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse, UserOut

router = APIRouter(prefix="/api/auth", tags=["Auth"])

@router.post("/register", response_model=TokenResponse)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    if db.query(User).filter((User.email == data.email) | (User.username == data.username)).first():
        raise HTTPException(409, "Email or username already exists")
    user = User(email=data.email, username=data.username, password_hash=hash_password(data.password))
    db.add(user)
    db.flush()
    db.add(Profile(user_id=user.id, full_name=data.username, bio=""))
    db.commit()
    return TokenResponse(access_token=create_token(user.id), user=user)

@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(401, "Invalid email or password")
    return TokenResponse(access_token=create_token(user.id), user=user)

@router.get("/me", response_model=UserOut)
def me(user=Depends(get_current_user)):
    return user
