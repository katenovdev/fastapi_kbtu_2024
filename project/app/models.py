from sqlmodel import SQLModel, Field
from pydantic import BaseModel
from typing import List

#USER

class UserBase(SQLModel):
    email: str
    password: str


class User(UserBase, table=True):
    id: int = Field(default=None, nullable=False, primary_key=True)

class UserCreate(BaseModel):
    email: str
    
class UserLogin(BaseModel):
    email: str
    password: str
    

class Author(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    full_name: str
    
class AuthorCreateM(BaseModel):
    full_name: str

class Genre(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    
class GenreCreateM(BaseModel):
    name: str

class Book(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    year_published: int
    author_id: int = Field(foreign_key="author.id")
    pages: int
    
class BookCreate(BaseModel):
    name: str
    year_published: int
    author_id: int
    pages: int
    genres: List[int]

class BookGenre(SQLModel, table=True):
    __tablename__ = "book_genre"
    book_id: int = Field(foreign_key="book.id", primary_key=True)
    genre_id: int = Field(foreign_key="genre.id", primary_key=True)
    
class UserBook(SQLModel, table=True):
    __tablename__ = "user_book"
    user_id: int = Field(foreign_key="user.id", primary_key=True)
    book_id: int = Field(foreign_key="book.id", primary_key=True)