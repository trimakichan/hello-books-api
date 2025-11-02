from flask import Blueprint, abort, make_response, request, Response
from app.models.book import Book
from ..db import db

books_bp = Blueprint("books_bp", __name__, url_prefix="/books")

@books_bp.post("")
def create_book():
    request_body = request.get_json()
    try:
        new_book = Book.from_dict(request_body)
    except KeyError as error:
        response = {"message": f"Invalid request: missing {error.args[0]}"}
        abort(make_response(response, 400))

    db.session.add(new_book)
    db.session.commit()

    return new_book.to_dict(), 201

@books_bp.get("")
def get_all_books():
    title_param = request.args.get("title")
    query = db.select(Book)

    if title_param:
        query = query.where(Book.title.ilike(f"%{title_param}%"))

    description_param = request.args.get("description")
    if description_param:
        query = query.where(Book.description.ilike(f"%{description_param}%"))
    
    query.order_by(Book.id)
    books = db.session.scalars(query)

    books_response = []
    for book in books:
        books_response.append(book.to_dict())
    return books_response

@books_bp.get("/<book_id>")
def get_one_book(book_id):
    book = validate_book(book_id)

    return book.to_dict()


@books_bp.put("/<book_id>")
def update_book(book_id):
    book = validate_book(book_id)
    request_body = request.get_json()

    try:
        title = request_body["title"]
        description = request_body["description"]
    except KeyError:
        msg = {"message": "please provide a valid title and description."}
        abort(make_response(msg, 400))

    book.title = title
    book.description = description
    db.session.commit()

    return Response(status=204,mimetype="application/json")

@books_bp.delete("/<book_id>")
def delete_book(book_id):
    book = validate_book(book_id)
    db.session.delete(book)
    db.session.commit()
    return Response(status=204, mimetype="application/json")

def validate_book(book_id):

    try:
        book_id = int(book_id)
    except ValueError:
        msg = {"message": f"Book {book_id} invalid."}
        abort(make_response(msg, 400))
    
    query = db.select(Book).where(Book.id == book_id)
    book = db.session.scalar(query)

    if book is None: # or if not book:
        msg = {"message": f"Book {book_id} is not found."}
        abort(make_response(msg, 404))

    return book

