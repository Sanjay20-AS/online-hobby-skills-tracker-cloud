from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import Post, Like, Comment, User
from app.schemas.domain import PostCreate, CommentCreate

router=APIRouter(prefix="/api/posts",tags=["Community"])

def serialize(post, db, current_user_id):
    user=db.get(User,post.user_id)
    likes=db.query(Like).filter(Like.post_id==post.id).count()
    comments=db.query(Comment).filter(Comment.post_id==post.id).count()
    liked=db.query(Like).filter(Like.post_id==post.id,Like.user_id==current_user_id).first() is not None
    return {"id":post.id,"user_id":post.user_id,"username":user.username,"content":post.content,
            "image_url":post.image_url,"created_at":post.created_at,"likes":likes,
            "comments":comments,"liked":liked}

@router.get("/feed")
def feed(user=Depends(get_current_user),db:Session=Depends(get_db)):
    posts=db.query(Post).order_by(Post.id.desc()).limit(50).all()
    return [serialize(p,db,user.id) for p in posts]

@router.post("")
def create_post(data:PostCreate,user=Depends(get_current_user),db:Session=Depends(get_db)):
    p=Post(user_id=user.id,**data.model_dump()); db.add(p); db.commit(); db.refresh(p)
    return serialize(p,db,user.id)

@router.delete("/{post_id}")
def delete_post(post_id:int,user=Depends(get_current_user),db:Session=Depends(get_db)):
    p=db.query(Post).filter(Post.id==post_id,Post.user_id==user.id).first()
    if not p: raise HTTPException(404,"Post not found")
    db.delete(p); db.commit(); return {"message":"Post deleted"}

@router.post("/{post_id}/like")
def toggle_like(post_id:int,user=Depends(get_current_user),db:Session=Depends(get_db)):
    p=db.get(Post,post_id)
    if not p: raise HTTPException(404,"Post not found")
    like=db.query(Like).filter(Like.post_id==post_id,Like.user_id==user.id).first()
    if like: db.delete(like); liked=False
    else: db.add(Like(post_id=post_id,user_id=user.id)); liked=True
    db.commit(); return {"liked":liked}

@router.get("/{post_id}/comments")
def comments(post_id:int,db:Session=Depends(get_db)):
    rows=db.query(Comment,User).join(User,Comment.user_id==User.id).filter(Comment.post_id==post_id).all()
    return [{"id":c.id,"username":u.username,"content":c.content} for c,u in rows]

@router.post("/{post_id}/comments")
def add_comment(post_id:int,data:CommentCreate,user=Depends(get_current_user),db:Session=Depends(get_db)):
    if not db.get(Post,post_id): raise HTTPException(404,"Post not found")
    c=Comment(post_id=post_id,user_id=user.id,content=data.content); db.add(c); db.commit(); db.refresh(c)
    return {"id":c.id,"content":c.content}
