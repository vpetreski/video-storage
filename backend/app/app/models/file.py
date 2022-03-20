from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String, DateTime

from app.db.base_class import Base


class File(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    size = Column(Integer)
    created_at = Column(DateTime, index=True)
