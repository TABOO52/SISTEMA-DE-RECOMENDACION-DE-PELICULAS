from fastapi import FastAPI
import pandas as pd

# Crear una instancia de la aplicación FastAPI
app = FastAPI()

#Cargar el Dataframe desde el archivo CSV 
df_movies = pd.read_csv('data/df_movies_limpio.csv')
df_credits_cast = pd.read_csv('data/df_credits_cast.csv')
df_credits_crew = pd.read_csv('data/df_credits_crew.csv')

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

@app.get('/votos_titulo/{titulo_de_la_filmacion}')
def votos_titulo(titulo_de_la_filmacion : str):
    titulo_de_la_filmacion = titulo_de_la_filmacion.lower()
    if titulo_de_la_filmacion in df_movies['title'].values:
        titulo = df_movies[df_movies['title'] == titulo_de_la_filmacion]['title'].iloc[0]
        año = df_movies[df_movies['title'] == titulo_de_la_filmacion]['release_year'].iloc[0] 
        total = df_movies[df_movies['title'] == titulo_de_la_filmacion]['vote_count'].iloc[0] 
        promedio = df_movies[df_movies['title'] == titulo_de_la_filmacion]['vote_average'].iloc[0] 
        return {'message': f'La pelicula {titulo} fue estrenada en el año {año}. La misma cuenta con un total de {total} valoraciones, con un promedio de {promedio}'}
    else:
        return {'error': 'Titulo de pelicula no valido. Por favor ingrese un titulo valido'}

@app.get('/exito_actor/{nombre_actor}')
def get_actor(nombre_actor : str):
    nombre_actor = nombre_actor.lower()

    df_filtered = df_credits_cast[df_credits_cast['cast_name'].apply(lambda x: nombre_actor in x)]
    cantidad_titulos = df_filtered.shape[0]
    total_return = df_filtered['return'].sum()
    promedio_return = df_filtered['return'].mean()
    if cantidad_titulos == 0:
        return {'message': f'Actor "{nombre_actor}" no encontrado en el dataset.'}
    return {'message': f'El actor {nombre_actor} ha participado de {cantidad_titulos} cantidad de filmaciones, el mismo ha conseguido un retorno de {total_return} con un promedio de {promedio_return} por filmacion.'}

@app.get('/exito_director/{nombre_director}')
def get_director(nombre_director : str):
    nombre_director = nombre_director.lower()
    if nombre_director in df_credits_crew['crew_name_directing'].values:
        df_filtered = df_credits_crew[df_credits_crew['crew_name_directing'] == nombre_director]
        nombre = df_credits_crew[df_credits_crew['crew_name_directing'] == nombre_director]['crew_name_directing'].iloc[0]  
        peliculas_director = {}
        for index, row in df_filtered.iterrows():
            peliculas_director[row['title']] = row['release_year']  
            
        return {'message': f'El director {nombre} ha participado en las peliculas {peliculas_director}.'}
    else:
        return {'error': 'Nombre del director no valido. Por favor ingrese un nombre valido'}
    