from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.auth import router as auth_router
from app.routers.reader import router as reader_router
from app.routers.books import router as book_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    auth_router,
    prefix="/api/auth",
    tags=["auth"]
)

app.include_router(
    reader_router,
    prefix="/api/reader",
    tags=["reader"]
)

app.include_router(
    book_router,
    prefix="/api/books",
    tags=["books"]
)
