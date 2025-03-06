from datetime import date
from pydantic import BaseModel
from typing import List, Optional


class MovieBase(BaseModel):
    name: str
    date: date
    score: float
    genre: str
    overview: str
    crew: str
    orig_title: str
    status: str
    orig_lang: str
    budget: float
    revenue: float
    country: str


class MovieCreate(MovieBase):
    pass


class Movie(MovieBase):
    id: int

    class Config:
        from_attributes = True


class MovieDetailResponseSchema(Movie):
    pass


class MovieListResponseSchema(BaseModel):
    movies: List[Movie]  # Исправлено на List[Movie]

    class Config:
        from_attributes = True


class MoviesPage(BaseModel):
    movies: List[Movie]  # Исправлено на List[Movie]
    prev_page: Optional[str]
    next_page: Optional[str]
    total_pages: int
    total_items: int
