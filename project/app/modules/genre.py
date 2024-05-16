from fastapi import APIRouter, Depends, HTTPException, Response
from app.config.config import SECRET_KEY
from app.models import GenreCreateM, Genre
from app.db import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from app.guard.jwt import get_current_user

router = APIRouter()

@router.post("/create/")
async def create_author(genre_data: GenreCreateM, current_user: str = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    genre = Genre(**genre_data.dict())
    session.add(genre)
    await session.commit()
    return genre

@router.get("/get-list", response_model=List[Genre])
async def get_authors(session: AsyncSession = Depends(get_session)):
    genre = await session.exec(select(Genre))
    return genre.scalars().all()

@router.get("/{genre_id}", response_model=Genre)
async def get_author_by_id(genre_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Genre).filter(Genre.id == genre_id))
    genre = result.scalars().first()

    if genre is None:
        raise HTTPException(status_code=404, detail="Genre not found")

    return genre