from datetime import datetime, timedelta
from typing import Union

from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import String

from .base import Base, db


class Role(Base):
    __tablename__ = "role"
    name = Column(String(80), unique=True)

    user = relationship("User", back_populates="role")

    @classmethod
    def get_by_name(
        cls,
        name: str,
    ) -> Union["Role", None]:
        """
        Get Role by name

        Args:
           name:

        Returns:
            Role
        """
        return db.session.query(cls).filter(Role.name == name).first()
