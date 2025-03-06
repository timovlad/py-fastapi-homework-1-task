from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from database import get_db, MovieModel
from schemas import (
    Movie,
    MovieCreate,
    MovieListResponseSchema,
    MovieDetailResponseSchema,
    MoviesPage,
)

router = APIRouter()


@router.post("/movies/", response_model=Movie)
async def create_movie(movie: MovieCreate, db: AsyncSession = Depends(get_db)):
    db_movie = MovieModel(**movie.dict())
    db.add(db_movie)
    await db.commit()
    await db.refresh(db_movie)
    return db_movie


@router.get("/movies/", response_model=MoviesPage)
async def read_movies(
    page: int = Query(1, ge=1, description="Page number, must be >= 1"),
    per_page: int = Query(
        10,
        ge=1,
        le=20,
        description="Number of items per page, must be between 1 and 20",
        alias="per_page",
        example=10,
    ),
    db: AsyncSession = Depends(get_db),
) -> MoviesPage:
    result = await db.execute(select(func.count(MovieModel.id)))
    total_items = result.scalar()
    total_pages = (total_items - 1) // per_page + 1

    if page > total_pages:
        raise HTTPException(status_code=404, detail="No movies found.")

    result = await db.execute(
        select(MovieModel).offset((page - 1) * per_page).limit(per_page)
    )
    movies = result.scalars().all()

    prev_page = f"/movies/?page={page - 1}&per_page={per_page}" if page > 1 else None
    next_page = (
        f"/movies/?page={page + 1}&per_page={per_page}" if page < total_pages else None
    )

    return MoviesPage(
        movies=movies,
        prev_page=prev_page,
        next_page=next_page,
        total_pages=total_pages,
        total_items=total_items,
    )


@router.get("/movies/{film_id}", response_model=MovieDetailResponseSchema)
async def get_movie(film_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(MovieModel).where(MovieModel.id == film_id))
    movie = result.scalar_one_or_none()
    if not movie:
        raise HTTPException(
            status_code=404, detail="Movie with the given ID was not found."
        )
    return movie
