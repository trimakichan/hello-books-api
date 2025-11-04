from flask import Blueprint, abort, make_response, request, Response
from app.models.book import Book
from app.models.author import Author
from .route_utilities import validate_model, create_model, get_models_with_filters
from ..db import db

bp = Blueprint("books_bp", __name__, url_prefix="/books")

@bp.post("")
def create_book():
    request_body = request.get_json()
    return create_model(Book, request_body)

@bp.get("")
def get_all_books():
    return get_models_with_filters(Book, request.args)

@bp.get("/<book_id>")
def get_one_book(book_id):
    book = validate_model(Book, book_id)

    return book.to_dict()


@bp.put("/<book_id>")
def update_book(book_id):
    book = validate_model(Book, book_id)
    request_body = request.get_json()
    author_id = request_body.get("author_id")
    if author_id:
        author = validate_model(Author, author_id)

    try:
        title = request_body["title"]
        description = request_body["description"]
    except KeyError:
        msg = {"message": "please provide a valid title and description."}
        abort(make_response(msg, 400))
    

    book.title = title
    book.description = description
    # double check if this is the right way.

    book.author_id = author.id if author_id else None

    db.session.commit()

    return Response(status=204,mimetype="application/json")

@bp.delete("/<book_id>")
def delete_book(book_id):
    book = validate_model(Book, book_id)
    db.session.delete(book)
    db.session.commit()
    return Response(status=204, mimetype="application/json")


# cat = {
#     "id": self.id,
#     "name":self.name,
#     "color": self.color,
#     "personality": self.personality
# }

