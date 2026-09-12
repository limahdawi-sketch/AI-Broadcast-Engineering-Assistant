import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, String, Text, DateTime
from .database import Base


def _uuid() -> str:
    return uuid.uuid4().hex


class KnowledgeEntry(Base):
    """
    A field-contributed fault report: cause + fix + notes, tied to an
    (optional) fault category. Mirrors the client-side Knowledge Bank in
    app/dsng-troubleshooter.html, but persisted server-side so it survives
    across devices/browsers instead of relying on artifact storage.

    validation_state follows the controlled-learning principle from
    ARCHITECTURE.md: a new entry is never "official" knowledge on its own --
    it starts as PENDING and must be explicitly reviewed and approved
    (Phase 3 feature; the review endpoint is a stub here, see api/knowledge.py).
    """
    __tablename__ = "knowledge_entries"

    id = Column(String, primary_key=True, default=_uuid)
    title = Column(String, nullable=False)
    category = Column(String, nullable=False, default="other")
    causes = Column(Text, nullable=False)
    fix = Column(Text, nullable=False)
    notes = Column(Text, nullable=True, default="")
    author = Column(String, nullable=False, default="Unspecified engineer")
    validation_state = Column(String, nullable=False, default="pending")  # pending | approved | rejected
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
