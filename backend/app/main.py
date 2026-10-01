from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from app.core.config import settings
from app.core.database import Base, engine
from app.routers import auth, profile, skills, goals, practice, posts, social, search, analytics, files
import app.models

Base.metadata.create_all(bind=engine)

app=FastAPI(title="Online Hobby & Skills Tracker API",version="1.0.0",
            description="Cloud-ready REST API for hobby, skill, goal, practice and community tracking.")

origins=[x.strip() for x in settings.cors_origins.split(",") if x.strip()]
app.add_middleware(CORSMiddleware,allow_origins=origins,allow_credentials=True,
                   allow_methods=["*"],allow_headers=["*"])

Path("uploads").mkdir(exist_ok=True)
app.mount("/uploads",StaticFiles(directory="uploads"),name="uploads")

app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(skills.router)
app.include_router(goals.router)
app.include_router(practice.router)
app.include_router(posts.router)
app.include_router(social.router)
app.include_router(search.router)
app.include_router(analytics.router)
app.include_router(files.router)

@app.get("/api/health")
def health():
    return {"status":"healthy","service":"hobby-skills-tracker-api"}
