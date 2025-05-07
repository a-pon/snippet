from datetime import datetime, UTC
from uuid import uuid4

from sqlalchemy import Column, ForeignKey, Integer, String, TIMESTAMP
from sqlalchemy.orm import relationship

from .base import Base


class Snippet(Base):
    __tablename__ = 'snippets'
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    uuid = Column(String(36), index=True, nullable=False, default=lambda: str(uuid4()))
    code = Column(String(256), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.now(UTC))
    author_id = Column(Integer, ForeignKey('user.id'))
    author = relationship('User', back_populates='snippets')
