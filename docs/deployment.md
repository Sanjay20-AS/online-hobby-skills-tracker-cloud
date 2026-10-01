# Deployment

1. Create a managed PostgreSQL database.
2. Set `DATABASE_URL` on the backend.
3. Set a strong random `JWT_SECRET`.
4. Deploy the backend with:
   `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Deploy the frontend as a static Vite application.
6. Set `VITE_API_URL` to the public backend URL.
7. Change `CORS_ORIGINS` to the public frontend URL.
8. Configure S3-compatible object storage for persistent uploads.
9. Test `/api/health` and `/docs`.
