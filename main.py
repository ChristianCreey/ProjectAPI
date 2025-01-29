# uvicorn main:app --reload --port 4000

from fastapi import FastAPI, Body, Path, Query, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional
from user_jwt import createToken, validateToken
from fastapi.security import HTTPBearer



app = FastAPI(
    title='Aprendiendo fast api',
    description='Una api en los primeros pasos',
    version='0.0.1',
)

#security = HTTPBearer()

class BearerJWT(HTTPBearer):
    #Crear una funcion asincrona
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validateToken(auth.credentials)
        if data['email'] != 'ccreey@outlook.es':
            raise HTTPException(status_code=403, detail='Credenciales incorrectas')
        return auth
 
class User(BaseModel):
    email: str = Field(default='correo@email.com')
    password: str = Field(default=**********)

class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(default='Titulo de la pelicula', min_length=5, max_length=50)
    overview: str = Field(default='Descripcion de la pelicula', min_length=5, max_length=500)
    year: int = Field(default=2000)
    rating: float = Field(ge=1, le=10)
    category: str = Field(default='Categoria de la pelicula', min_length=5, max_length=50)

movies = [
    {
        'id': 1,
        'title': 'Transformes',
        'overview': 'Los autobots tienen que defender la tierra de los decepticos',
        'year': 2009,
        'rating': 9.9,
        'category': 'Accion'
    },
    {
        'id': 2,
        'title': 'Iron man',
        'overview': 'El hombre de hierro',
        'year': 2010,
        'rating': 10,
        'category': 'Ciencia ficcion'
    }
]

@app.post('/login', tags=['autentication'])
def login(user: User):
    if user.email == 'ccreey@outlook.es' and user.password == '12345':
        token: str = createToken(user.model_dump()) #user.dict() ya no es válido en las versiones recientes de Pydantic (usar model_dump() en Pydantic v2).
        #print(token)
        #print(user)
        return JSONResponse(content={'access_token': token})
    raise HTTPException(status_code=401, detail="Credenciales incorrectas")


@app.get('/', tags=['Inicio'])
def read_root():
    return HTMLResponse('<h2>Hola mundo</h2>')

@app.get('/movies', tags=['Movies'], dependencies=[Depends(BearerJWT())]) #colocar en las funciones que queramos que este autenticado para ver las movies (dependencies=[Depends(BearerJWT())])
def get_movies():
        return JSONResponse(content=movies)

@app.get('/movies/{id}', tags=['Movies'])
def get_movie(id: int = Path(ge=1, le=100)):
    for item in movies:
        if item["id"] == id:
            return item
    raise HTTPException(status_code=404, detail="Película no encontrada")


#PARAMETROS QUERY
#BUSQUEDA POR CATEGORIA
@app.get('/movies/category', tags=['Movies'])
def get_movies_by_category(category: str = Query(min_length=5, max_length=50)):
    #return category
    return JSONResponse(content=[movie for movie in movies if movie['category'].lower() == category.lower()])


#Metodo post
@app.post('/movies', tags=['Movies'], status_code=201)
def create_movie(movie: Movie):
    #asignar un id unico automaticamente
    new_id = len(movies)+1
    movie_dict = movie.model_dump() #convertir el objeto movie a diccionario
    movie_dict["id"] = new_id
    movies.append(movie_dict)
    print(movie_dict)
    return JSONResponse(status_code=201, content={'message':'se ha cargado una nueva pelicula', 'movies':movie_dict})
    #return JSONResponse(status_code=201, content={'message':'se ha cargado una nueva pelicula', 'movie':[movies.dict() for movie in movies]})

#Metodo put
@app.put('/movies/{id}', tags=['Movies'], status_code=200)
def update_movie(id: int, movie: Movie):
    for item in movies:
        if item['id'] == id:
            item.update(movie.model_dump())
            return JSONResponse(content={'message': 'Se ha modificado la película', 'movie': item})
    raise HTTPException(status_code=404, detail="Pelicula no encontrada")

#metodo delete
@app.delete('/movies/{id}', tags=['Movies'], status_code=200)
def delete_movie(id: int):
    for item in movies:
        if item['id'] == id:
            movies.remove(item)
            print(movies)
            return JSONResponse(content={'message':'se ha eliminado la pelicula'})
    raise HTTPException(status_code=404, detail="Pelicula no encontrada")


#esquema de validacion

#docker run -it --rm -p 4000:4000 projectapi