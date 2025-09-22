from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
import asyncio
from crud import (
    create_book, create_chapter, create_chunk,
    get_book, get_chapter,
    get_all_books, get_all_chapters_bookid, get_all_chunks_chapter
)
from models import UserBooks

app = FastAPI(title="StudyAI", version="0.1.0")

@app.post("/upload")
async def upload_textbook(file: UploadFile = File(...)):
    pdf_bytes = await file.read()

@app.get("/upload")
async def get_uploaded_textbooks():
    books = await get_all_books()
    user_books = UserBooks()
