# uvicorn main:app --reload --port 4000

from fastapi import FastAPI, Body, Path, Query
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI(
    title='Aprendiendo fast api',
    description='Una api en los primeros pasos',
    version='0.0.1',
)

class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(default='Titulo de la pelicula', min_lenght=5, max_length=50)
    overview: str = Field(default='Descripcion de la pelicula', min_lenght=5, max_length=500)
    year: int = Field(default=2023)
    rating: float = Field(ge=1, le=10)
    category: str = Field(default='Categoria de la pelicula', min_lenght=5, max_length=50)

movies = [
    {
        'id': 1,
        'title': 'Transformes',
        'overview': 'Los autobots tienen que defender la tierra de los decepticos',
        'year': '2009',
        'rating': 9.9,
        'category': 'Accion'
    },
    {
        'id': 2,
        'title': 'Iron mas',
        'overview': 'El hombre de hierro',
        'year': '2010',
        'rating': 10,
        'category': 'Guerra'
    }
]

@app.get('/', tags=['Inicio'])
def read_root():
    return HTMLResponse('<h2>Hola mundo</h2>')

@app.get('/movies', tags=['Movies'])
def get_movies():
        return JSONResponse(content=movies)

@app.get('/movies/{id}', tags=['Movies'])
def get_movie(id: int = Path(ge=1, le=100)):
    for item in movies:
        if item['id'] == id:
            return item
    return []

#PARAMETROS QUERY
#BUSQUEDA POR CATEGORIA
@app.get('/movies/', tags=['Movies'])
def get_movies_by_category(category: str = Query(min_length=5, max_length=50)):
    return category

#Metodo post
@app.post('/movies', tags=['Movies'], status_code=200)
def create_movie(movie: Movie):
    movies.append(movie)
    print(movies)
    return JSONResponse(status_code=201, content={'message':'se ha cargado una nueva pelicula', 'movie':[movie.dict() for m in movies]})

#Metodo put
@app.put('/movies/{id}', tags=['Movies'], status_code=200)
def update_movie(id: int, movie: Movie):
    for item in movies:
        if item['id'] == id:
            item['title'] = movie.title
            item['overview'] = movie.overview
            item['year'] = movie.year
            item['rating'] = movie.rating
            item['category'] = movie.category
            return JSONResponse(content={'mesagge': 'se ha modificado la pelicula'})

#metodo delete
@app.delete('/movies/{id}', tags=['Movies'], status_code=200)
def delete_movie(id: int):
    for item in movies:
        if item['id'] == id:
            movies.remove(item)
            return JSONResponse(content={'message':'se ha eliminado la pelicula'})


#esquema de validacion