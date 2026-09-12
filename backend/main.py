"""AI Broadcast Engineering Assistant - Phase 2 integrated local backend."""
from contextlib import asynccontextmanager
from pathlib import Path
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from models.database import init_db
from api import diagnostic, knowledge, equipment, assistant

BASE_DIR = Path(__file__).resolve().parents[1]
APP_FILE = BASE_DIR / "app" / "dsng-troubleshooter.html"

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(
    title="AI Broadcast Engineering Assistant API",
    description="Phase 2 integrated backend -- Earth Station / DSNG engineering support.",
    version="0.2.1",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000", "http://localhost:8000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(diagnostic.router)
app.include_router(knowledge.router)
app.include_router(equipment.router)
app.include_router(assistant.router)

@app.get("/health", tags=["meta"])
def health():
    return {"status": "ok", "service": "ai-broadcast-engineering-assistant", "version": app.version}

@app.get("/", include_in_schema=False)
def root():
    return FileResponse(APP_FILE)

@app.get("/dsng-troubleshooter.html", include_in_schema=False)
def app_file():
    return FileResponse(APP_FILE)

# Expose the app directory as static content for any future assets.
app.mount("/app", StaticFiles(directory=str(BASE_DIR / "app")), name="app-static")
