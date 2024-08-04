import logging
from functools import wraps

import jwt
from flask import g, request
from werkzeug.exceptions import Unauthorized

from config import settings
from model.endpoint import Endpoint
from model.user import User


def auth(value: str):
    """
    Authorize user

    Args:
        value: value to check if used as @auth(value) otherwise callable

    Raises:
        Unauthorized: Authorization Missing, Invalid Token or Unauthorized user

    Returns:
        Decorated function
    """

    def decorator(f):
        @wraps(f)
        def wrapper_function(*args, **kwargs):
            g.user = None

            logging.info(f"Permission is {value}")

            authorization = request.headers.get("Authorization")
            env = settings.env
            if not authorization:
                err = {"status": "nok", "errors": ["Authorization Missing."]}
                raise Unauthorized(err)
            if authorization.startswith("Basic ") and env in ["dev", "testing"]:
                email = authorization.split("Basic ")[1]
                g.user = User.get_by_email(email)

            else:
                token = authorization.split("Bearer ")
                if token and len(token) == 2:
                    token = token[1]
                    SECRET_KEY = settings.secret_key

                    try:
                        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
                        g.user = User.get_by_id(payload["user_id"])

                        logging.info(f"payload {payload} ")

                        role_id = payload["role_id"]
                        logging.info(f"role_id {role_id}")

                    except jwt.ExpiredSignatureError:
                        raise Unauthorized(
                            {"status": "nok", "errors": ["Token has expired."]}
                        )
                    except jwt.InvalidTokenError:
                        raise Unauthorized(
                            {"status": "nok", "errors": ["Invalid token."]}
                        )

                if g.user:
                    required_roles = Endpoint.get_roles_for_route(value)
                    logging.info(f"req roles {required_roles}")
                    if role_id in required_roles:
                        logging.info("Allowed as role_id exists in required Roles ")
                        return f(*args, **kwargs)

            raise Unauthorized({"status": "nok", "errors": ["Unauthorized user."]})

        return wrapper_function

    if callable(value):
        f = value
        return decorator(f)

    return decorator
