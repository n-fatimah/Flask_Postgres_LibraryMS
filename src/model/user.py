import hashlib
import logging
from datetime import datetime, timedelta
from typing import Union

import jwt
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String

from common.enums import DefaultRole

from .base import Base, db


class User(Base):
    username = Column(String(80), unique=True)
    email = Column(String(120), unique=True)
    password = Column(String(64), unique=True)

    role_id = Column(
        Integer,
        ForeignKey("role.id"),
        nullable=False,
        default=DefaultRole.CUSTOMER.value,
    )

    issued_books = relationship("IssuedBook", back_populates="user")
    role = relationship("Role", back_populates="user")

    @classmethod
    def get_by_email(cls, email: str) -> Union["User", None]:
        """
        Get user by email

        Args:
            email: user email

        Returns:
            User
        """
        row = db.session.query(cls).filter(User.email == email).first()
        return row

    @classmethod
    def check_password(cls, stored_password: str, provided_password: str) -> bool:
        """
        Check if the provided password matches the stored hashed password

        Args:
            stored_password: The hashed password stored in the database
            provided_password: The password provided by the user

        Returns:
            bool: True if the passwords match, False otherwise
        """
        return stored_password == hashlib.sha256(provided_password.encode()).hexdigest()
