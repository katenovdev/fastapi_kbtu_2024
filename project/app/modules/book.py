from fastapi import APIRouter, Depends, HTTPException
from app.models import Book, BookGenre, BookCreate, Author, Genre
from app.db import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List


router = APIRouter()

@router.post("/create/")
async def create_book(book_data: BookCreate, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Author).filter(Author.id == book_data.author_id))
    author = result.scalars().first()

    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    genreres = await session.exec(select(Genre))
    genre = genreres.scalars().all()
    genre_ids = [g.id for g in genre]

    if any(genre_id not in genre_ids for genre_id in book_data.genres):
        raise HTTPException(status_code=404, detail="One or more genres not found")

    book = Book(**book_data.dict())
    session.add(book)
    await session.commit()

    return {"message": "Book created successfully"}

@router.get("/get-list/", response_model=List[Book])
async def get_books(session: AsyncSession = Depends(get_session)):
    # Retrieve all books from the database
    books = await session.execute(select(Book))
    return books.scalars().all()

@router.get("/{book_id}", response_model=Book)
async def get_book_by_id(book_id: int, session: AsyncSession = Depends(get_session)):
    # Retrieve the book from the database by its ID
    book = await session.execute(select(Book).filter(Book.id == book_id).limit(1))
    book_obj = book.scalars().first()

    # If the book doesn't exist, raise an HTTPException with status code 404 (Not Found)
    if book_obj is None:
        raise HTTPException(status_code=404, detail="Book not found")

    return book_obj