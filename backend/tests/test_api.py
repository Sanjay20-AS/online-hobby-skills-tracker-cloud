import os
os.environ["DATABASE_URL"]="sqlite:///./test_hobbytracker.db"
os.environ["JWT_SECRET"]="test-secret"
os.environ["CORS_ORIGINS"]="http://testserver"

from fastapi.testclient import TestClient
from app.main import app

client=TestClient(app)

def unique():
    import uuid
    return uuid.uuid4().hex[:8]

def test_register_login_and_skill():
    tag=unique()
    email=f"{tag}@example.com"
    r=client.post("/api/auth/register",json={"email":email,"username":tag,"password":"Password@123"})
    assert r.status_code==200
    token=r.json()["access_token"]
    headers={"Authorization":f"Bearer {token}"}
    r=client.post("/api/skills",headers=headers,json={"name":"Python","category":"Programming"})
    assert r.status_code==200
    assert r.json()["name"]=="Python"

def test_health():
    r=client.get("/api/health")
    assert r.status_code==200
    assert r.json()["status"]=="healthy"
