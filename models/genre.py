from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, validates
from . import Base, CRUDMixin

class Genre(CRUDMixin, Base):
    tablename = "genres"