from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    username = Column(String(256), unique=True, nullable=False)
    email = Column(String(128), index=True, unique=True, nullable=False)
    hashed_password = Column(String(1024), nullable=False)
    salt = Column(String(1024), index=True, unique=True, nullable=False)
    role_id = Column(Integer, ForeignKey('role.id'))
    role = relationship('Role', back_populates='users')
    snippets = relationship('Snippet', back_populates='author')
