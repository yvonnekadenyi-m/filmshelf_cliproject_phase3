from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, ForeignKey, DateTime, UniqueConstraint
)
from sqlalchemy.orm import relationship, validates
from . import Base, CRUDMixin


class Movie(CRUDMixin, Base):
    __tablename__ = "movies"
    __table_args__ = (
        UniqueConstraint("title", "genre_id", name="uq_movie_title_genre"),
    )

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False, index=True)
    genre_id = Column(Integer, ForeignKey("genres.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    genre = relationship("Genre", back_populates="movies")
    reviews = relationship(
        "Review",
        back_populates="movie",
        cascade="all, delete-orphan"
    )

    @validates("title")
    def validate_title(self, _, value):
        cleaned = (value or "").strip()
        if not cleaned:
            raise ValueError("Title cannot be empty.")
        if len(cleaned) > 200:
            raise ValueError("Title must be 200 characters or less.")
        return cleaned

    def __repr__(self):
        return f"<Movie id={self.id} title={self.title!r} genre_id={self.genre_id}>"