"""
SQLite for now, by design (see ARCHITECTURE.md). The engine/session pattern
here is deliberately PostgreSQL-compatible so swapping DATABASE_URL later is
a one-line change, not a rewrite.
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./data/app.db")

if DATABASE_URL.startswith("sqlite:///"):
    _db_path = DATABASE_URL.replace("sqlite:///", "", 1)
    _db_dir = os.path.dirname(_db_path)
    if _db_dir:
        os.makedirs(_db_dir, exist_ok=True)

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    # Imported here (not at module top) to avoid circular imports between
    # models and database at startup.
    from . import knowledge, equipment  # noqa: F401
    Base.metadata.create_all(bind=engine)
