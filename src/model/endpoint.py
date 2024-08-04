from typing import Union

from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import ARRAY, Integer, String

from .base import Base, db


class Endpoint(Base):
    __tablename__ = "endpoint"
    route = Column(String(120), unique=True)
    method = Column(String(25), unique=True)
    roles = Column(ARRAY(Integer), nullable=False)

    @classmethod
    def get_by_route_method(cls, route: str, method: str) -> Union["Endpoint", None]:
        """
        Get Endpoint by route and method

        Args:
            route:
            method:

        Returns:
            Endpoint
        """

        return (
            db.session.query(cls)
            .filter(Endpoint.route == route, Endpoint.method == method)
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
        endpoint = db.session.query(cls).filter(Endpoint.route == route).first()
        if endpoint:
            return endpoint.roles
        return []
