from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class Book(Base):
    __tablename__="books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=True)
    chapters = relationship("Chapter", back_populates="book")

class Chapter(Base):
    __tablename__ = "chapters"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    title = Column(String, nullable=False)
    order = Column(Integer, nullable=True)
    start_page = Column(String, nullable=False)
    #end_page = Column(String, nullable=False)

    book = relationship("Book", back_populates="chapters")
    chunks = relationship("Chunk", back_populates="chapter")

class Chunk(Base):
    __tablename__ = "chunks"

    id = Column(Integer, primary_key=True, index=True)
    chapter_id = Column(Integer, ForeignKey("chapters.id"))
    order = Column(Integer, nullable=False)
    title = Column(String, nullable=True)
    text = Column(Text, primary_key=True, index=True)
    start_page = Column(String, nullable=False)
    #end_page = Column(String, nullable=False)

    chapter = relationship("Chapter", back_populates="chunks")
    images = relationship("Image", back_populates="chunk")

class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    chunk_id = Column(Integer, ForeignKey("chunks.id"))
    path = Column(String, nullable=False)

    chunk = relationship("Chunk", back_populates="images")

