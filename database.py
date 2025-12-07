import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# Prefer env DATABASE_URL; default to local SQLite file
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///watchlist.db")

# Create engine
engine = create_engine(DATABASE_URL, echo=False, future=True)

# Session factory
# autocommit kwarg removed; use simple sessionmaker defaults
SessionLocal = sessionmaker(bind=engine, autoflush=False)


def init_db():
    """Import models and create tables"""
    # import modules so SQLAlchemy picks up the model classes
    import models.user  # noqa: F401
    import models.movie  # noqa: F401
    import models.review  # noqa: F401
    import models.genre  # noqa: F401


Base.metadata.create_all(bind=engine)
