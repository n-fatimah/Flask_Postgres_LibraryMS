import logging
from http import HTTPStatus

from flask import Blueprint
from flask_restx import Api
from werkzeug.exceptions import Unauthorized

from .user.endpoints import api as user_api
from .book.endpoints import api as book_api
from .issued_book.endpoints import api as issued_book_api
from .role.endpoints import api as role_api
from .endpoint.endpoints import api as endpoint_api

# from .access.endpoints import api as access_api

blueprint = Blueprint("api", __name__)

authorizations = {
    "Authorization": {
        "description": "",
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
    }
}

api = Api(
    blueprint,
    title="Flask Boilerplate API",
    version="0.1",
    description="Flask Boilerplate APIs",
    authorizations=authorizations,
    security="Authorization",
)

api.add_namespace(user_api)
api.add_namespace(book_api)
api.add_namespace(issued_book_api)
api.add_namespace(role_api)
api.add_namespace(endpoint_api)
# api.add_namespace(access_api)


@api.errorhandler(Unauthorized)
def handle_unauthorized_error(exception_cause):
    """
    Catch unauthorized exceptions globally and respond with 401.

    Args:
        exception_cause: Cause

    Returns:
        Response
    """
    logging.exception(exception_cause)
    return exception_cause.description, HTTPStatus.UNAUTHORIZED
