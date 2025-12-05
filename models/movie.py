from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, ForeignKey, DateTime, UniqueConstraint
)
from sqlalchemy.orm import relationship, validates
from . import Base, CRUDMixin

class Movie(CRUDMixin, Base):
    tablename = "movies"
    table_args = (
        UniqueConstraint("title", "genre_id", name="uq_movie_title_genre"),
    )

