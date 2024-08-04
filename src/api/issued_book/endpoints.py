from http import HTTPStatus
from typing import Dict, Tuple

from flask import request
from flask_restx import Resource

from api.issued_book import schemas
from helpers.responses import failure_response, success_response
from model.book import Book
from model.issued_book import IssuedBook
from model.user import User

from . import api


@api.route("/")
class IssueBook(Resource):
    @api.doc("Issue a book")
    @api.expect(schemas.issued_book_expect, validate=True)
    @api.marshal_with(schemas.issued_book_response, skip_none=True)
    def post(self) -> Tuple[Dict, int]:
        """
        Issue a book to a user

        Returns:
            Issued Book
        """
        api.logger.info("Issue book")

        book = Book.get_by_id(api.payload["book_id"])
        if not book:
            return failure_response(["Book not found."], HTTPStatus.NOT_FOUND)

        if book.available_quantity <= 0:
            return failure_response(["Book not available."], HTTPStatus.BAD_REQUEST)

        user = User.get_by_id(api.payload["user_id"])
        if not user:
            return failure_response(["User not found."], HTTPStatus.BAD_REQUEST)

        issued_book = IssuedBook(**api.payload).insert()

        new_quantity = book.available_quantity - 1

        Book.update(book.id, {"available_quantity": new_quantity})

        return success_response(issued_book, HTTPStatus.CREATED)

    @api.doc("List issued books")
    @api.param("page")
    @api.param("per_page")
    @api.marshal_list_with(schemas.issued_book_response, skip_none=True)
    def get(self) -> Tuple[Dict, int]:
        """
        Get all Issued Books

        Returns:
            List of users
        """
        page = request.args.get("page", default=1, type=int)
        per_page = request.args.get("per_page", default=4, type=int)
        api.logger.info("List users")
        books = IssuedBook.get_all_issued_books(page=page, per_page=per_page)
        return success_response(books, HTTPStatus.OK)


@api.route("/<int:book_id>")
class BookDetails(Resource):
    @api.doc("Get book details including user info")
    @api.param("page")
    @api.param("per_page")
    @api.marshal_with(schemas.issued_book_response, skip_none=True)
    def get(self, book_id: int) -> Tuple[Dict, int]:
        """
        Get details of a book including the user who issued it.

        Args:
            book_id: The ID of the book.

        Returns:
            Book details including user information if issued.
        """
        api.logger.info(f"Get book details with ID: {book_id}")
        page = request.args.get("page", default=1, type=int)
        per_page = request.args.get("per_page", default=2, type=int)
        issued_book = IssuedBook.get_book_details_with_user(book_id, page, per_page)

        return success_response(issued_book, HTTPStatus.OK)


@api.route("/<int:user_id>/")
class UserBooks(Resource):
    @api.doc("Get all books issued by a user")
    @api.param("page")
    @api.param("per_page")
    @api.marshal_with(schemas.issued_book_response, skip_none=True)
    def get(self, user_id: int) -> Tuple[Dict, int]:
        """
        Get all books issued by a user.

        Args:
            user_id: The ID of the user.

        Returns:
            List of books issued by the user.
        """
        api.logger.info(f"Get book details issued by a user with ID: {user_id}")
        page = request.args.get("page", default=1, type=int)
        per_page = request.args.get("per_page", default=2, type=int)
        issued_books = IssuedBook.get_books_issued_by_user(user_id, page, per_page)
        return success_response(issued_books, HTTPStatus.OK)
