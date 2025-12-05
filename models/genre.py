from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, validates
from . import Base, CRUDMixin

class Genre(CRUDMixin, Base):
    tablename = "genres"

    id = Column(Integer, primary_key=True)
name = Column(String(80), unique=True, nullable=False, index=True)

movies = relationship("Movie", back_populates="genre")

@validates("name")
def validate_name(self, _, value):
    cleaned = (value or "").strip()
    if not cleaned:
        raise ValueError("Genre name cannot be empty.")
    if len(cleaned) > 80:
        raise ValueError("Genre name must be 80 characters or less.")
    return cleaned

def __repr__(self):
    return f"<Genre id={self.id} name={self.name!r}>"