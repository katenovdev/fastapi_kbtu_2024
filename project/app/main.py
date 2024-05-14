from fastapi import FastAPI

from app.modules.user import router as user_router
from app.modules.author import router as author_router

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)


app.include_router(user_router, prefix="/user", tags=["users"])
app.include_router(author_router, prefix="/author", tags=["users"])

