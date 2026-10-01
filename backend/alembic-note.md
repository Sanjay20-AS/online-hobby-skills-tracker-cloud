For a production deployment, add Alembic migrations rather than relying on `Base.metadata.create_all()`.

Example migration workflow:

```bash
pip install alembic
alembic init migrations
alembic revision --autogenerate -m "initial schema"
alembic upgrade head
```

The current starter deliberately uses automatic table creation to keep local setup beginner-friendly.
