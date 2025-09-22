import fitz
import logging
from models import (
    Book,
    Chapter,
    Chunk,
)
from crud import (
    create_book, create_chapter, create_chunk,
    get_book, get_chapter,
    get_all_books, get_all_chapters_bookid, get_all_chunks_chapter
)
import re

def table_of_contents(pdf_bytes: bytes):
    doc = fitz.open(pdf_bytes)
    toc = doc.get_toc()
    metadata = doc.metadata
    logging.debug("Extracted table of contents and metadata.")
    return toc, metadata

def parse_pdf(pdf_bytes):
    toc, metadata = table_of_contents(pdf_bytes)

    if toc is None:
        logging.error("PDF has no TOC.")
        return
    
    if "title" or "author" not in metadata:
        logging.warning("title or author not in metadata")
        return
    
    # Create book
    book = Book(
        title=metadata.get("title"),
        author=metadata.get("author"),
    )
    book = create_book(book)

    # Create chapters
    current_chapter = None
    current_chunk_order = 1
    for level, title, page in toc:
        # Chapters
        if level == 0:
            match = re.search(r"chapter (\d+)", title, re.IGNORECASE).group(0)
            order = match.group(1) if match else None
            chapter = Chapter(
                book_id=book.id,
                title=title,
                order = order,
                start_page=page
            )
            chapter = create_chapter(chapter)
            current_chapter = chapter
            current_chunk_order = 1
        else:
            chunk = Chunk(
                chapter_id = current_chapter.id,
                order=current_chunk_order,
                title=title,
                # raw text=?
                start_page=page,
            )
            chunk = create_chunk(chunk)
            current_chunk_order += 1

