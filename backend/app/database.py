from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, String, Text, Integer, create_engine, select, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from .config import get_settings
from .schemas import utcnow


class Base(DeclarativeBase):
    pass


class ResearchRun(Base):
    __tablename__ = "research_runs"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    condition: Mapped[str] = mapped_column(String(120))
    status: Mapped[str] = mapped_column(String(32), default="queued", index=True)
    mode: Mapped[str] = mapped_column(String(16))
    policy_version: Mapped[str] = mapped_column(String(50))
    request: Mapped[dict] = mapped_column(JSONB)
    result: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class SourceSnapshot(Base):
    __tablename__ = "source_snapshots"
    id: Mapped[str] = mapped_column(String(90), primary_key=True)
    source: Mapped[str] = mapped_column(String(30))
    canonical_id: Mapped[str] = mapped_column(String(40), index=True)
    content_hash: Mapped[str] = mapped_column(String(64))
    data: Mapped[dict] = mapped_column(JSONB)
    captured_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class Citation(Base):
    __tablename__ = "citations"
    id: Mapped[str] = mapped_column(String(60), primary_key=True)
    run_id: Mapped[str] = mapped_column(ForeignKey("research_runs.id", ondelete="CASCADE"), index=True)
    snapshot_id: Mapped[str] = mapped_column(ForeignKey("source_snapshots.id"))
    data: Mapped[dict] = mapped_column(JSONB)


class EvidencePassage(Base):
    __tablename__ = "evidence_passages"
    id: Mapped[str] = mapped_column(String(80), primary_key=True)
    citation_id: Mapped[str] = mapped_column(ForeignKey("citations.id", ondelete="CASCADE"), index=True)
    snapshot_id: Mapped[str] = mapped_column(ForeignKey("source_snapshots.id"))
    locator: Mapped[str] = mapped_column(Text)
    text: Mapped[str] = mapped_column(Text)


class ClaimRecord(Base):
    __tablename__ = "claims"
    id: Mapped[str] = mapped_column(String(60), primary_key=True)
    run_id: Mapped[str] = mapped_column(ForeignKey("research_runs.id", ondelete="CASCADE"), index=True)
    data: Mapped[dict] = mapped_column(JSONB)


class ClaimEvidence(Base):
    __tablename__ = "claim_evidence"
    claim_id: Mapped[str] = mapped_column(ForeignKey("claims.id", ondelete="CASCADE"), primary_key=True)
    evidence_id: Mapped[str] = mapped_column(ForeignKey("evidence_passages.id"), primary_key=True)
    quote: Mapped[str] = mapped_column(Text)
    check: Mapped[dict] = mapped_column(JSONB)


class ConflictRecord(Base):
    __tablename__ = "conflicts"
    id: Mapped[str] = mapped_column(String(60), primary_key=True)
    run_id: Mapped[str] = mapped_column(ForeignKey("research_runs.id", ondelete="CASCADE"), index=True)
    data: Mapped[dict] = mapped_column(JSONB)


class RunEvent(Base):
    __tablename__ = "run_events"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    run_id: Mapped[str] = mapped_column(ForeignKey("research_runs.id", ondelete="CASCADE"), index=True)
    stage: Mapped[str] = mapped_column(String(40))
    message: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


def make_engine(url: str | None = None):
    url = url or get_settings().database_url.get_secret_value()
    if not url.startswith("postgresql"):
        raise ValueError("This service requires PostgreSQL.")
    return create_engine(url, pool_pre_ping=True, hide_parameters=True, connect_args={"connect_timeout": 5})


engine = make_engine()
Session = sessionmaker(engine, expire_on_commit=False)


def create_schema():
    # Serialize prototype bootstrap across a CLI smoke run and local server start.
    with engine.begin() as connection:
        connection.execute(text("SELECT pg_advisory_xact_lock(27102601)"))
        Base.metadata.create_all(connection)


def initialize():
    create_schema()
    with Session.begin() as db:
        for run in db.scalars(select(ResearchRun).where(ResearchRun.status.in_(["queued", "running"]))):
            run.status = "interrupted"
            run.finished_at = utcnow()
            db.add(
                RunEvent(
                    run_id=run.id,
                    stage="interrupted",
                    message="Local worker restarted. Start a new run to retry.",
                )
            )


def event(run_id: str, stage: str, message: str):
    with Session.begin() as db:
        db.add(RunEvent(run_id=run_id, stage=stage, message=message))
