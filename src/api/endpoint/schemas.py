from flask_restx.fields import Integer, List, Nested, String

from . import api

endpoint = api.model(
    "endpoint",
    {"id": Integer(), "route": String(), "method": String(), "role_id": Integer()},
)

endpoint_expect = api.model(
    "endpoint_expect",
    {
        "route": String(required=True),
        "method": String(required=True),
        "role_id": Integer(min=1),
    },
    strict=True,
)

endpoint_response = api.model(
    "endpoint_response",
    {
        "status": String(description="ok|nok"),
        "data": Nested(endpoint, skip_none=True, allow_null=True),
        "errors": List(String),
    },
)
