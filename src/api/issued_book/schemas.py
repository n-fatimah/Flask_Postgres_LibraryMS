from flask_restx.fields import Integer, List, Nested, String

from . import api

# from book.schemas import book
# from user.schemas import user

user = api.model(
    "user",
    {"id": Integer(), "username": String(), "email": String(), "created_at": String()},
)

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

issued_book = api.model(
    "issued_book",
    {
        "id": Integer(),
        "book_id": Integer(),
        "user_id": Integer(),
        "status": String(),
        "book": Nested(book, skip_none=True),
        "user": Nested(user, skip_none=True),
    },
)
issued_book_expect = api.model(
    "issued_book_expect",
    {
        "book_id": Integer(required=True),
        "user_id": Integer(required=True),
    },
    strict=True,
)

issued_book_response = api.model(
    "issued_book_response",
    {
        "status": String(description="ok|nok"),
        "data": Nested(issued_book, skip_none=True, allow_null=True, as_list=True),
        "errors": List(String),
    },
)
