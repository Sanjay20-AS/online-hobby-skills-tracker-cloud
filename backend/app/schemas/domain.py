from pydantic import BaseModel, Field
from app.schemas.common import ORMModel

class ProfileUpdate(BaseModel):
    full_name: str = ""
    bio: str = ""

class SkillCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    category: str = "General"
    current_level: str = "Beginner"
    target_level: str = "Intermediate"
    description: str = ""

class SkillOut(SkillCreate, ORMModel):
    id: int
    user_id: int

class GoalCreate(BaseModel):
    title: str = Field(min_length=1, max_length=160)
    description: str = ""
    skill_id: int | None = None
    target_value: float = 100
    current_value: float = 0
    deadline: str | None = None
    status: str = "active"

class GoalOut(GoalCreate, ORMModel):
    id: int
    user_id: int

class MilestoneCreate(BaseModel):
    title: str
    description: str = ""

class MilestoneOut(MilestoneCreate, ORMModel):
    id: int
    goal_id: int
    completed: bool

class PracticeCreate(BaseModel):
    skill_id: int | None = None
    duration_minutes: int = Field(ge=1, le=1440)
    activity: str = Field(min_length=1, max_length=200)
    notes: str = ""
    practice_date: str

class PracticeOut(PracticeCreate, ORMModel):
    id: int
    user_id: int

class PostCreate(BaseModel):
    content: str = Field(min_length=1, max_length=5000)
    skill_id: int | None = None

class CommentCreate(BaseModel):
    content: str = Field(min_length=1, max_length=1000)

class SearchResult(BaseModel):
    type: str
    id: int
    label: str
