# Online Hobby & Skills Tracker with Community Sharing on Cloud

A cloud-ready full-stack project for tracking hobbies, skills, learning goals, practice sessions, milestones and achievements, with a community feed and cloud/object-storage support.

## Stack

- Frontend: React + Vite + CSS
- Backend: Python + FastAPI
- Database: PostgreSQL (SQLite also works locally)
- ORM: SQLAlchemy
- Auth: JWT + bcrypt
- Object storage: local filesystem by default; S3-compatible storage supported through environment variables
- Testing: Pytest + FastAPI TestClient
- Docker: Docker Compose
- CI: GitHub Actions

## Features

- Registration/login with JWT authentication
- User profiles
- Skills and hobbies
- Learning goals and milestones
- Practice-session tracking
- Progress and analytics
- Achievement posts
- Likes and comments
- Follow/unfollow
- Search users and skills
- Proof/image/file upload
- Ownership-based authorization
- Health endpoint
- Swagger/OpenAPI docs
- Local SQLite mode
- PostgreSQL/Docker mode
- Optional S3-compatible object storage
- Automated backend tests

## 1. Run locally without Docker

### Backend

```bash
cd backend
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt
copy .env.example .env   # Windows
# cp .env.example .env   # Linux/macOS

uvicorn app.main:app --reload
```

Backend:
- API: http://127.0.0.1:8000
- Swagger: http://127.0.0.1:8000/docs

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend:
- http://localhost:5173

The default backend database is SQLite, so PostgreSQL is not required for the first local run.

## 2. Docker

From the project root:

```bash
docker compose up --build
```

Then open:
- Frontend: http://localhost:5173
- Backend: http://localhost:8000/docs

Docker starts PostgreSQL automatically.

## 3. Demo accounts

Run the seed script after starting the backend:

```bash
cd backend
python seed.py
```

Demo users:

```text
arun@example.com / Demo@123
meena@example.com / Demo@123
```

All data is synthetic.

## 4. Cloud deployment

### Database

Create a PostgreSQL database such as Supabase PostgreSQL and set:

```env
DATABASE_URL=postgresql+psycopg://USER:PASSWORD@HOST:5432/postgres
```

### Backend

Deploy `backend/` to a Python-capable service such as Render.

Build command:

```bash
pip install -r requirements.txt
```

Start command:

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Set:

```env
DATABASE_URL=...
JWT_SECRET=long-random-secret
CORS_ORIGINS=https://your-frontend-domain.example
```

### Frontend

Build:

```bash
npm run build
```

Set:

```env
VITE_API_URL=https://your-backend-domain.example
```

Deploy the generated `dist/` directory to a static hosting provider.

## 5. Object storage

The project works locally without a cloud storage account.

For production, use any S3-compatible object storage. Set:

```env
S3_ENDPOINT_URL=
S3_ACCESS_KEY=
S3_SECRET_KEY=
S3_BUCKET=hobby-tracker
S3_REGION=us-east-1
```

If these variables are absent, uploaded files are stored in `backend/uploads/`.

Do not put cloud service-role credentials in the React frontend.

## Architecture

```text
                 Browser
                    |
                 HTTPS
                    |
             React Frontend
                    |
                REST API
                    |
              FastAPI Backend
             /       |       \
            /        |        \
         Auth    PostgreSQL   Object Storage
          |          |            |
        JWT      User data    Proof/media
```

The API is stateless. Persistent data is outside the application process, making the backend suitable for horizontal scaling.

## Main API groups

```text
POST /api/auth/register
POST /api/auth/login
GET  /api/auth/me

GET/PUT /api/profile

GET/POST/PUT/DELETE /api/skills
GET/POST/PUT/DELETE /api/goals
POST/PUT/DELETE /api/milestones
GET/POST /api/practice
GET /api/analytics/overview

GET/POST /api/posts
POST/DELETE /api/posts/{id}/like
GET/POST /api/posts/{id}/comments

POST/DELETE /api/users/{id}/follow
GET /api/search

POST /api/files/upload
GET /api/health
```

## Security

- Passwords are hashed with bcrypt.
- JWT tokens are signed with a server-side secret.
- Protected endpoints require authentication.
- Resource ownership is checked before updates/deletes.
- CORS is configurable.
- Uploads have type and size restrictions.
- Secrets belong in environment variables.
- `.env` is ignored by Git.

## Suggested GitHub proof

Use meaningful commits:

```text
feat: initialize FastAPI backend
feat: add JWT authentication
feat: add skills and goals
feat: add practice tracking
feat: add analytics
feat: add community feed
feat: add object storage adapter
test: add authorization tests
ci: add GitHub Actions
docker: add local PostgreSQL stack
docs: add cloud deployment guide
```

## Screenshots to capture

1. Login
2. Dashboard
3. Skills
4. Goals/milestones
5. Practice tracking
6. Analytics
7. Community feed
8. Create post
9. File upload
10. Swagger API
11. GitHub Actions
12. Cloud deployment

## Cloud-computing concepts demonstrated

- Cloud-hosted web application
- Managed PostgreSQL
- Object storage
- Authentication and authorization
- REST APIs
- Stateless application architecture
- Containerization
- CI/CD
- Multi-device persistent data
- Horizontal scalability design
- Security controls
- Automated testing

## License

Educational project. Synthetic demo data only.
