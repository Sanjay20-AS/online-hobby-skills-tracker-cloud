from app.core.database import Base, engine, SessionLocal
from app.core.security import hash_password
from app.models.user import User, Profile, Skill, Goal, PracticeSession, Post

Base.metadata.create_all(bind=engine)
db=SessionLocal()

def get_or_create(email,username):
    u=db.query(User).filter(User.email==email).first()
    if not u:
        u=User(email=email,username=username,password_hash=hash_password("Demo@123"))
        db.add(u); db.flush(); db.add(Profile(user_id=u.id,full_name=username.title(),bio="Synthetic demo user"))
    return u

arun=get_or_create("arun@example.com","arun")
meena=get_or_create("meena@example.com","meena")
db.commit()

if not db.query(Skill).filter(Skill.user_id==arun.id).first():
    py=Skill(user_id=arun.id,name="Python",category="Programming",current_level="Intermediate",target_level="Advanced",description="Backend and automation")
    ph=Skill(user_id=arun.id,name="Photography",category="Creative",current_level="Beginner",target_level="Intermediate")
    db.add_all([py,ph]); db.flush()
    db.add(Goal(user_id=arun.id,skill_id=py.id,title="Solve 50 Python problems",target_value=50,current_value=32,status="active"))
    db.add_all([
        PracticeSession(user_id=arun.id,skill_id=py.id,duration_minutes=60,activity="FastAPI practice",notes="Built REST endpoints",practice_date="2026-10-01"),
        Post(user_id=arun.id,content="Completed another milestone in my Python learning journey!")
    ])
    db.commit()
print("Seed complete. Demo password: Demo@123")
db.close()
