"""
app/models/base.py
Shared DeclarativeBase for all SQLAlchemy ORM models.
All models import Base from here.
"""
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass