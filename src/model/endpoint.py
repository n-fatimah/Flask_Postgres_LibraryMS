# from typing import Union

from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String

from common.enums import DefaultRole

from .base import Base, db


class Endpoint(Base):
    __tablename__ = "endpoint"
    route = Column(String(120), unique=False)
    method = Column(String(25), unique=False)

    role_id = Column(
        Integer,
        ForeignKey("role.id"),
        nullable=True,
        default=DefaultRole.CUSTOMER.value,
    )

    role = relationship("Role", back_populates="endpoint")

    @classmethod
    def get_by_route_method_role_id(
        cls, route: str, method: str, role_id: int
    ) :#-> Union["Endpoint", None]:
        """
        Get Endpoint by route ,method and role id

        Args:
            route:
            method:

        Returns:
            Endpoint
        """

        return (
            db.session.query(cls)
            .filter(
                Endpoint.route == route,
                Endpoint.method == method,
                Endpoint.role_id == role_id,
            )
            .first()
        )

    @classmethod
    def get_roles_for_route(cls, route: str):
        """
        Fetch roles associated with a specific route.

        Args:
            route: The route for which to fetch roles.

        Returns:
            List of role IDs associated with the route.
        """
        return db.session.query(cls).filter(Endpoint.route == route).all()
