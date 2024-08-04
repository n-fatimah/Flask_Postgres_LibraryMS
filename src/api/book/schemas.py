from flask_restx.fields import Integer, List, Nested, String

from . import api

book = api.model(
    "book",
    {
        "id": Integer(),
        "title": String(),
        "author": String(),
        "quantity": Integer(),
        "available_quantity": Integer(),
    },
)
book_expect = api.model(
    "book_expect",
    {
        "title": String(required=True),
        "author": String(required=True),
        "quantity": Integer(required=True, min=1),
    },
    strict=True,
)

book_response = api.model(
    "book_response",
    {
        "status": String(description="ok|nok"),
        "data": Nested(book, skip_none=True, allow_null=True),
        "errors": List(String),
    },
)


book_update_expect = api.model(
    "book_update_expect",
    {
        "title": String(required=False),
        "author": String(required=False),
        "quantity": Integer(required=False, min=1),
    },
)


update_book_response = api.model(
    "update_book_response",
    {
        "status": String(description="ok|nok"),
        "data": Nested(book, skip_none=True, allow_null=True),
        "errors": List(String),
    },
)
