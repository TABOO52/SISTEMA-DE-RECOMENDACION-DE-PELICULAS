from fastapi import FastAPI
import pandas as pd

# Crear una instancia de la aplicación FastAPI
app = FastAPI()

#Cargar el Dataframe desde el archivo CSV 
df_movies = pd.read_csv('data/df_movies_limpio.csv')


# Definir una ruta y una función para manejarla
@app.get('/')
def read_root():
    return {"message": "Hello, World Render!"}

@app.get('/cantidad_filmaciones_mes/{mes}')
def cantidad_filmaciones_mes(mes: str):
    mes = mes.lower()  # Convertir el mes a minúsculas para evitar problemas de mayúsculas/minúsculas
    if mes in df_movies['release_month'].unique():
        # Filtrar las películas estrenadas en el mes consultado
        cantidad = df_movies[df_movies['release_month'] == mes].shape[0]
        return {"message": f"{cantidad} cantidad de películas fueron estrenadas en el mes de {mes}"}
    else:
        return {"error": "Mes no válido. Por favor ingrese un mes en español válido."}

@app.get('/cantidad_filmaciones_dia/{dia}')
def cantidad_filmaciones_dia(dia: str):
    dia = dia.lower()
    if dia in df_movies['release_day'].unique():
        cantidad = df_movies[df_movies['release_day'] == dia].shape[0]
        return {'message': f'{cantidad} cantidad de peliculas fueron estrenadas en los dias {dia}'}
    else:
        return {'error': 'Dia no valido. Por favor ingrese un dia en español válido.'}
    
@app.get('/popularidad_estreno/{titulo_de_la_filmacion}')
def score_titulo(titulo_de_la_filmacion: str):
    titulo_de_la_filmacion = titulo_de_la_filmacion.lower()
    if titulo_de_la_filmacion in df_movies['title'].values:
        titulo = df_movies[df_movies['title'] == titulo_de_la_filmacion]['title'].iloc[0]  
        año = df_movies[df_movies['title'] == titulo_de_la_filmacion]['release_year'].iloc[0]  
        popularidad = df_movies[df_movies['title'] == titulo_de_la_filmacion]['popularity'].iloc[0]  
        return {'message': f'La pelicula {titulo} fue estrenada en el año {año} con un score/popularidad de {popularidad}'}
    else:
        return {'error': 'Titulo de pelicula no valido. Por favor ingrese un titulo valido'}