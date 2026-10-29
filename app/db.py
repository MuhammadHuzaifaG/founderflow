from datetime import datetime, timezone
from sqlalchemy import (
    Boolean, Column, DateTime, Float, ForeignKey, Integer, JSON, String, Text, create_engine
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

from app.config import get_settings

Base = declarative_base()
settings = get_settings()

DATABASE_URL = settings.database_url

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is required. Set it in Vercel environment variables.")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class FounderTaskRecord(Base):
    __tablename__ = "founder_tasks"

    id = Column(Integer, primary_key=True, index=True)
    task_type = Column(String(80), nullable=False)
    company_name = Column(String(120), nullable=False)
    market = Column(String(200), nullable=False)
    founder_goal = Column(Text, nullable=False)
    context = Column(Text, nullable=True)
    summary = Column(Text, nullable=False)
    findings = Column(JSON, nullable=False, default=list)
    recommended_next_steps = Column(JSON, nullable=False, default=list)
    confidence = Column(Float, nullable=False, default=0.0)
    human_judgment_required = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    notes = relationship("DecisionNoteRecord", back_populates="task", cascade="all, delete-orphan")

    def to_public_dict(self):
        return {
            "id": self.id,
            "task_type": self.task_type,
            "company_name": self.company_name,
            "market": self.market,
            "founder_goal": self.founder_goal,
            "context": self.context,
            "summary": self.summary,
            "findings": self.findings or [],
            "recommended_next_steps": self.recommended_next_steps or [],
            "confidence": self.confidence,
            "human_judgment_required": self.human_judgment_required,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

class DecisionNoteRecord(Base):
    __tablename__ = "decision_notes"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("founder_tasks.id"), nullable=False)
    note_title = Column(String(120), nullable=False)
    note_body = Column(Text, nullable=False)
    decision_flag = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    task = relationship("FounderTaskRecord", back_populates="notes")

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()