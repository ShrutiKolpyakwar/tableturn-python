
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from tableturn.settings import Settings

Base = declarative_base()

engine = None
SessionLocal = None


def configure_database():
    """Configure the engine using the current environment settings."""
    global engine, SessionLocal

    settings = Settings()

    connect_args = {}
    if settings.database_url.startswith("sqlite"):
        connect_args = {"check_same_thread": False}

    engine = create_engine(
        settings.database_url,
        connect_args=connect_args,
    )

    SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )

    return engine


def get_db():
    """Provide a database session and close it after use."""
    if SessionLocal is None:
        configure_database()

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()