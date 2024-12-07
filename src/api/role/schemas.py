from flask_restx.fields import Integer, List, Nested, String

from . import api

role = api.model(
    "user",
    {"id": Integer(), "name": String()},
)

role_expect = api.model(
    "role_expect",
    {"name": String(required=True)},
    strict=True,
)

role_response = api.model(
    "user_response",
    {
        "status": String(description="ok|nok"),
        "data": Nested(role, skip_none=True, allow_null=True),
        "errors": List(String),
    },
)
