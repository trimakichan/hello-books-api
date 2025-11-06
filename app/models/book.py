from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import Optional
from typing import TYPE_CHECKING
from ..db import db

if TYPE_CHECKING:
    from .author import Author
    
class Book(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    author_id: Mapped[Optional[int]] = mapped_column(ForeignKey("author.id"))
    author: Mapped[Optional["Author"]] = relationship(back_populates="books")
    genres: Mapped[list["Genre"]] = relationship(secondary="book_genre", back_populates="books")


    def to_dict(self):
        book_as_dict = {
            "id": self.id,
            "title": self.title,
            "description": self.description
        }

        if self.author:
            book_as_dict["author"] = self.author.name
        
        if self.genres:
            book_as_dict["genres"] = [genre.name for genre in self.genres]

        return book_as_dict
    

    @classmethod
    def from_dict(cls, book_data):
        author_id = book_data.get("author_id")
        genres = book_data.get("genres", [])
        new_book = cls(title=book_data["title"],
                        description=book_data["description"],
                        author_id=author_id,
                        genres=genres
                        )

        return new_book

# class Book():
#     def __init__(self,id, title, description):
#         self.id = id
#         self.title = title
#         self.description = description


# books = [
#     Book(1, "Fictional Book", "A fantasy novel set in an imaginary world."),
#     Book(2, "Wheel of Time", "A fantasy novel set in an imaginary world."),
#     Book(3, "Fictional Book Title", "A fantasy novel set in an imaginary world.")
# ]