import uuid
from sqlalchemy import (
    Column, String, DateTime, Boolean, ForeignKey
)
from sqlalchemy.dialects.postgresql import UUID, ENUM
from sqlalchemy.sql import func
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    contact = Column(String(50), nullable=True)
    email = Column(String(255), unique=True, nullable=False)
    company = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_active = Column(Boolean, nullable=False, default=True)
    is_verified = Column(Boolean, nullable=False, default=False)
    last_login = Column(DateTime(timezone=True), nullable=True)

class Auth(Base):
    __tablename__ = "auth"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), primary_key=True)
    encrypted_password = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    role = Column(
        ENUM("operator", "manager", name="user_role_enum"),
        nullable=False
    )
