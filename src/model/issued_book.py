from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import DateTime, Integer, String

from common.enums import BookStatus

from .base import Base, db


class IssuedBook(Base):
    __tablename__ = "issued_books"
    book_id = Column(Integer, ForeignKey("book.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    status = Column(String(50), nullable=False, default=BookStatus.ISSUED_BOOK.value)
    returned_at = Column(DateTime, nullable=True)

    book = relationship("Book", back_populates="issued_books")
    user = relationship("User", back_populates="issued_books")

    @classmethod
    def get_all_issued_books(cls, page: int, per_page: int):
        """
        Get all issued books

        Returns:
            List
        """

        return (
            db.session.query(cls)
            .filter(cls.status == BookStatus.ISSUED_BOOK.value)
            .offset((page - 1) * per_page)
            .limit(per_page)
            .all()
        )

    @classmethod
    def get_book_details_with_user(cls, book_id: int, page: int, per_page: int):
        """
        Get the details of a book with user information if issued.

        Args:
            book_id: The ID of the book.

        Returns:
            IssuedBook instance with book and user relationship.
        """
        return (
            db.session.query(cls)
            .filter(cls.book_id == book_id, cls.status == BookStatus.ISSUED_BOOK.value)
            .offset((page - 1) * per_page)
            .limit(per_page)
            .all()
        )

    @classmethod
    def get_books_issued_by_user(cls, user_id: int, page: int, per_page: int):
        """
        Get all books issued by a specific user.

        Args:
            user_id: The ID of the user.

        Returns:
            List of IssuedBook instances with book information.
        """
        return (
            db.session.query(cls)
            .filter(cls.user_id == user_id)
            .offset((page - 1) * per_page)
            .limit(per_page)
            .all()
        )
