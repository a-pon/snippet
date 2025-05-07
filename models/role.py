import enum

from sqlalchemy import Column, Enum, Integer
from sqlalchemy.orm import relationship

from .base import Base


class RoleEnum(enum.Enum):
    ADMIN = 'admin'
    USER = 'user'


class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name = Column(Enum(RoleEnum), unique=True, nullable=False)
    users = relationship('User', back_populates='role')
