from fastapi import APIRouter, Depends, HTTPException, Response
from app.config.config import SECRET_KEY
from app.models import AuthorCreateM, Author
from app.db import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from app.guard.jwt import get_current_user

router = APIRouter()

@router.post("/create/")
async def create_author(author_data: AuthorCreateM, current_user: str = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    author = Author(**author_data.dict())
    session.add(author)
    await session.commit()
    return author

@router.get("/authors/", response_model=List[Author])
async def get_authors(session: AsyncSession = Depends(get_session)):
    authors = await session.exec(select(Author))
    return authors.scalars().all()