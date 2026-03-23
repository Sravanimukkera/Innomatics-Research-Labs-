from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

# models
class Movie(BaseModel):
    id: int
    name: str = Field(..., min_length=2)
    rating: float = Field(..., ge=0, le=10)

class Ticket(BaseModel):
    id: int
    movie_id: int
    seats: int = Field(..., gt=0)

# storage
movies = []
tickets = []

# ------------------ MOVIES ------------------

# add movie
@app.post("/movies")
def add_movie(movie: Movie):
    for m in movies:
        if m.id == movie.id:
            raise HTTPException(400, "Movie already exists")
    movies.append(movie)
    return {"msg": "added"}


# get all movies
@app.get("/movies")
def get_movies():
    return movies


# pagination (IMPORTANT: keep before movie_id)
@app.get("/movies/page")
def page(page: int = 1, limit: int = 2):
    start = (page - 1) * limit
    end = start + limit
    return movies[start:end]


# get one movie
@app.get("/movies/{movie_id}")
def get_movie(movie_id: int):
    for m in movies:
        if m.id == movie_id:
            return m
    raise HTTPException(404, "not found")


# update movie
@app.put("/movies/{movie_id}")
def update_movie(movie_id: int, movie: Movie):
    for i in range(len(movies)):
        if movies[i].id == movie_id:
            movies[i] = movie
            return {"msg": "updated"}
    raise HTTPException(404, "not found")


# delete movie
@app.delete("/movies/{movie_id}")
def delete_movie(movie_id: int):
    for i in range(len(movies)):
        if movies[i].id == movie_id:
            movies.pop(i)
            return {"msg": "deleted"}
    raise HTTPException(404, "not found")


# ------------------ EXTRA ------------------

# search
@app.get("/search")
def search(name: str):
    return [m for m in movies if name.lower() in m.name.lower()]


# sort
@app.get("/sort")
def sort_movies():
    return sorted(movies, key=lambda x: x.rating, reverse=True)


# ------------------ TICKETS ------------------

# book ticket
@app.post("/book")
def book(ticket: Ticket):
    for m in movies:
        if m.id == ticket.movie_id:
            tickets.append(ticket)
            return {"msg": "booked"}
    raise HTTPException(404, "movie not found")


# get tickets
@app.get("/tickets")
def get_tickets():
    return tickets


# checkout
@app.post("/checkout")
def checkout():
    if not tickets:
        return {"msg": "no tickets"}
    return {"msg": "success", "tickets": tickets}