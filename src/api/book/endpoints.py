from http import HTTPStatus
from typing import Dict, Tuple

from flask import request
from flask_restx import Resource

from api.book import schemas
from helpers.responses import failure_response, success_response
from model.book import Book

from . import api


@api.route("/")
class BookList(Resource):
    @api.doc("Add a book")
    @api.expect(schemas.book_expect, validate=True)
    @api.marshal_list_with(schemas.book_response, skip_none=True)
    def post(self) -> Tuple[Dict, int]:
        """
        Add a new book

        Returns:
            Book
        """
        api.logger.info("Add book")
        book = Book.get_by_title_author(api.payload["title"], api.payload["author"])

        if book:
            err = "Either Book already exists"
            return failure_response(err, HTTPStatus.BAD_REQUEST)

        api.payload["available_quantity"] = api.payload["quantity"]
        book = Book(**api.payload).insert()
        return success_response(book, HTTPStatus.CREATED)

    @api.doc("List available books")
    @api.param("page")
    @api.param("per_page")
    @api.marshal_list_with(schemas.book_response, skip_none=True)
    def get(self) -> Tuple[Dict, int]:
        """
        Get all available books

        Returns:
            List of available books
        """
        api.logger.info("List available books")
        page = request.args.get("page", default=1, type=int)
        per_page = request.args.get("per_page", default=4, type=int)
        books = Book.get_all_available(page, per_page)
        return success_response(books, HTTPStatus.OK)


@api.route("/<int:book_id>")
class UpdateBook(Resource):
    @api.doc("Update a book")
    @api.expect(schemas.book_update_expect, validate=False)
    @api.marshal_with(schemas.update_book_response, skip_none=True)
    def patch(self, book_id: int) -> Tuple[Dict, int]:
        """
        Update a book

        Args:
            book_id: ID of the book to update

        Returns:
            Updated Book
        """
        api.logger.info(f"Updating the book with id : {book_id}")
        api.logger.info(f"Payload: {api.payload}")

        book = Book.get_by_id(book_id)
        if not book:
            return failure_response(["Book not found."], HTTPStatus.NOT_FOUND)

        if "quantity" in api.payload:
            if api.payload["quantity"] < book.available_quantity:
                return failure_response(
                    [
                        "Quantity should be greater than or equal to available quantity of books"
                    ],
                    HTTPStatus.BAD_REQUEST,
                )

        if "title" not in api.payload:
            api.payload["title"] = book.title

        if "author" not in api.payload:
            api.payload["author"] = book.author

        if Book.get_by_title_author(
            api.payload["title"], api.payload["author"], book_id
        ):
            return failure_response(
                "Book with same title and author already exists", HTTPStatus.BAD_REQUEST
            )

        Book.update(book_id, api.payload)

        updated_book = Book.get_by_id(book_id)
        return success_response(updated_book, HTTPStatus.OK)

    @api.doc("Get a book by ID")
    @api.marshal_with(schemas.book_response, skip_none=True)
    def get(self, book_id: int) -> Tuple[Dict, int]:
        """
        Get a book by its ID

        Args:
            book_id: ID of the book to retrieve

        Returns:
            Book details
        """
        api.logger.info(f"Get book with ID: {book_id}")

        book = Book.get_by_id(book_id)
        if not book:
            return failure_response(["Book Not Found."], HTTPStatus.NOT_FOUND)

        return success_response(book, HTTPStatus.OK)
