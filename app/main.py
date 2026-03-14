from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.api.v1.routes_auth import router as auth_router
from app.api.v1.routes_users import router as users_router
from app.api.v1.routes_vehicles import router as vehicles_router
from app.core.config import settings
from app.core.database import get_db

app = FastAPI(
    title=settings.project_name,
    description="Backend API for vehicle maintenance tracking",
    version=settings.version,
    debug=settings.debug,
)

app.include_router(users_router, prefix="/api/v1")
app.include_router(auth_router, prefix="/api/v1")
app.include_router(vehicles_router, prefix="/api/v1")


@app.get("/")
def read_root():
    return {"message": f"Welcome to {settings.project_name}"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/db-check")
def db_check(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"message": "database connection successful"}


@app.get("/tables-check")
def tables_check(db: Session = Depends(get_db)):
    result = db.execute(
        text("SELECT tablename FROM pg_tables WHERE schemaname = 'public'")
    )
    tables = [row[0] for row in result]
    return {"tables": tables}