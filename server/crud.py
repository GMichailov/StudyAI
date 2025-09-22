from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Book, Chapter, Chunk, Image
import os
from contextlib import contextmanager
import logging

DATABASE_URL = "sqlite:///./studyai.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

if "studyai.db" not in os.listdir(os.curdir):
    Base.metadata.create_all(bind=engine)

@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Books

async def create_book(book: Book):
    with get_db() as db:
        try:
            db.add(book)
            db.commit()
            db.refresh(book)
            logging.debug(f"Added book: {book.title}.")
            return book
        except Exception as e:
            db.rollback()
            logging.error(f"Failed to add book: {book.title}")

async def get_all_books():
    with get_db() as db:
        return db.query(Book).all()

async def get_book(book_id):
    with get_db() as db:
        try:
            return db.query(Book).filter(book_id==book_id)
        except Exception:
            logging.debug(f"Failed to get book: {book_id}")

async def delete_book_id(book_id):
    with get_db() as db:
        try:
            book = db.query(Book).filter(Book.id == book_id).first()
            if book:
                db.delete(book)
                db.commit()
                logging.debug(f"Delete book: {book.title}")
                return
            logging.debug(f"Book doesn't exist.")
        except Exception:
            logging.error('Failed to delete book.')

async def delete_book_title(title):
    with get_db() as db:
        try:
            book = db.query(Book).filter(Book.title == title).first()
            if book:
                db.delete(book)
                db.commit()
                logging.debug(f"Delete book: {book.title}")
                return
            logging.debug(f"Book doesn't exist.")
        except Exception:
            logging.error('Failed to delete book.')

# Chapters

async def create_chapter(chapter: Chapter):
    with get_db() as db:
        try:
            db.add(chapter)
            db.commit()
            db.refresh(chapter)
            logging.debug(f"Added chapter: {chapter.title}.")
            return chapter
        except Exception as e:
            db.rollback()
            logging.error(f"Failed to add chapter: {chapter.title}")

async def get_all_chapters_bookid(book_id):
    with get_db() as db:
        return db.query(Chapter).filter(book_id=book_id).all()

async def get_chapter(chapter_id):
    with get_db() as db:
        try:
            chapter = db.query().filter(chapter_id==chapter_id)
            if chapter:
                logging.debug(f"Successfully got chapter: {chapter.chapter_id}")
                return chapter
            logging.debug("Chapter does not exist.")
        except:
            logging.error("Failed to get chapter.")

async def delete_chapter_id(chapter_id):
    with get_db() as db:
        try:
            chapter = db.query(chapter).filter(chapter.id == chapter_id).first()
            if chapter:
                db.delete(chapter)
                db.commit()
                logging.debug(f"Delete chapter: {chapter.title}")
                return
            logging.debug(f"chapter doesn't exist.")
        except Exception:
            logging.error('Failed to delete chapter.')

# Chunks

async def create_chunk(chunk: Chunk):
    with get_db() as db:
        try:
            db.add(chunk)
            db.commit()
            db.refresh(chunk)
            logging.debug(f"Added chunk: {chunk.start_page}.")
            return chunk
        except Exception as e:
            db.rollback()
            logging.error(f"Failed to add chunk: {chunk.start_page}")

async def get_all_chunks_chapter(chapter_id):
    with get_db() as db:
        return db.query(Chunk).filter(chapter_id=chapter_id).all()

async def get_chunk(): pass

async def delete_chunk_id(chunk_id):
    with get_db() as db:
        try:
            chunk = db.query(chunk).filter(chunk.id == chunk_id).first()
            if chunk:
                db.delete(chunk)
                db.commit()
                logging.debug(f"Delete chunk: {chunk.start_page}")
                return
            logging.debug(f"chunk doesn't exist.")
        except Exception:
            logging.error('Failed to delete chunk.')


# Images