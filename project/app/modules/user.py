from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_session, init_db
from app.guard.jwt import get_current_user
import string
import secrets
import bcrypt
from datetime import datetime, timedelta
import jwt
from app.config.config import SECRET_KEY

from app.models import UserCreate, UserLogin, UserBook
from app.models import User, Book
from app.tasks import generate_and_send_password_email

router = APIRouter()


@router.post("/create/")
async def create_user(user_create: UserCreate, session: AsyncSession = Depends(get_session)):
    existing_user = await session.exec(select(User).where(User.email == user_create.email))
    if existing_user.first():
        raise HTTPException(status_code=400, detail="Email already registered")

    password_length = 12
    random_password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(password_length))

    task = generate_and_send_password_email.send(user_create.email, random_password)
    
    hashed_password = bcrypt.hashpw(random_password.encode('utf-8'), bcrypt.gensalt())

    user = User(email=user_create.email, password=hashed_password.decode('utf-8')) 
    session.add(user)
    await session.commit()

    return task

@router.post("/login/")
async def user_login(user_login: UserLogin, response: Response, session: AsyncSession = Depends(get_session)):
    
    user_result = await session.exec(select(User).where(User.email == user_login.email))
    user = user_result.scalars().first()
    
    if not user or not bcrypt.checkpw(user_login.password.encode('utf-8'), user.password.encode('utf-8')):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    token_data = {
        "id": str(user.id),
        "exp": datetime.utcnow() + timedelta(minutes=120)
    }
    token = jwt.encode(token_data, SECRET_KEY, algorithm="HS256")
    
    response.set_cookie(key="auth", value=token, httponly=True)

    return {"message": "Login successful"}

@router.get("/authme/")
async def auth_me(current_user: str = Depends(get_current_user)):
    return {
        "message": "SUCCESS",
        "statusCode": 200,
        "user": current_user
    }
    
    
@router.post("/add-book/{book_id}")
async def add_book_to_user(book_id: int, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    book = await session.execute(select(Book).filter(Book.id == book_id).limit(1))
    book_obj = book.scalars().first()
    
    if not book_obj:
        raise HTTPException(status_code=404, detail="Book not found")

    user_book = await session.execute(select(UserBook).filter_by(user_id=current_user, book_id=book_id))
    if user_book.scalar():
        raise HTTPException(status_code=400, detail="User already has this book")

    # Create the relationship between the user and the book
    user_book_relationship = UserBook(user_id=current_user, book_id=book_id)
    session.add(user_book_relationship)
    await session.commit()

    return {"message": "Book added to user successfully"}

@router.get("/get-favourites/")
async def get_user_books(current_user: int = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    user_books = await session.execute(select(Book).join(UserBook).filter(UserBook.user_id == current_user))
    user_books = user_books.scalars().all()

    return user_books