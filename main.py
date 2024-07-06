from fastapi import FastAPI, Request
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
from sklearn.decomposition import TruncatedSVD
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from functools import lru_cache

app = FastAPI()

templates = Jinja2Templates(directory="templates")

df_movies = pd.read_csv('data/df_movies_limpio.csv')
df_credits_cast = pd.read_csv('data/df_credits_cast.csv')
df_credits_crew = pd.read_csv('data/df_credits_crew.csv')

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Vectorización y reducción de dimensionalidad fuera de la función
title_vectorizer = TfidfVectorizer(max_df=0.8, min_df=10, max_features=200)
title_tfidf_matrix = title_vectorizer.fit_transform(df_movies['title'])

svd_title = TruncatedSVD(n_components=100)
title_tfidf_reduced = svd_title.fit_transform(title_tfidf_matrix)

company_vectorizer = TfidfVectorizer(max_df=0.8, min_df=10, max_features=200)
company_tfidf_matrix = company_vectorizer.fit_transform(df_movies['company_name'])

svd_company = TruncatedSVD(n_components=100)
company_tfidf_reduced = svd_company.fit_transform(company_tfidf_matrix)


@app.get('/cantidad_filmaciones_mes/{mes}')
def cantidad_filmaciones_mes(mes: str):
    '''Retorna la cantidad de peliculas estrenadas en ese mes.
    
    Args:
        mes (str)
    '''

    mes = mes.lower()
    if mes in df_movies['release_month'].unique():
        cantidad = df_movies[df_movies['release_month'] == mes].shape[0]
        return {"message": f"{cantidad} cantidad de películas fueron estrenadas en el mes de {mes}"}
    else:
        return {"error": "Mes no válido. Por favor ingrese un mes en español válido."}

@app.get('/cantidad_filmaciones_dia/{dia}')
def cantidad_filmaciones_dia(dia: str):
    '''Retorna la cantidad de peliculas estrenadas en ese dia.

    Args:
        dia (str)
    '''
    
    dia = dia.lower()
    if dia in df_movies['release_day'].unique():
        cantidad = df_movies[df_movies['release_day'] == dia].shape[0]
        return {'message': f'{cantidad} cantidad de peliculas fueron estrenadas en los dias {dia}'}
    else:
        return {'error': 'Dia no valido. Por favor ingrese un dia en español válido.'}
    
@app.get('/popularidad_estreno/{titulo_de_la_filmacion}')
def score_titulo(titulo_de_la_filmacion: str):
    '''Retorna el nombre de la pelicula y su popularidad
    
    Args:
        titulo_de_la_filmacion (str)
    '''
    
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
    '''Retorna el nombre de la pelicula junto a sus valoraciones mayores a 2000 votos.
    
    Args:
        titulo_de_la_filmacion
    '''
    
    titulo_de_la_filmacion = titulo_de_la_filmacion.lower()
    if titulo_de_la_filmacion in df_movies['title'].values:
        movie_row = df_movies[df_movies['title'] == titulo_de_la_filmacion]
        total_votes = movie_row['vote_count'].iloc[0]
        
        if total_votes >= 2000:
            titulo = movie_row['title'].iloc[0]
            año = movie_row['release_year'].iloc[0]
            promedio = movie_row['vote_average'].iloc[0]
            return {'message': f'La película {titulo} fue estrenada en el año {año}. La misma cuenta con un total de {total_votes} valoraciones, con un promedio de {promedio}'}
        else:
            return {'error': 'La película no tiene suficientes valoraciones (menos de 2000).'}
    else:
        return {'error': 'Título de película no válido. Por favor ingrese un título válido.'}

@app.get('/exito_actor/{nombre_actor}')
def get_actor(nombre_actor : str):
    '''Retorna el nombre del actor y varios detalles del exito en sus peliculas
    
    Args:
        nombre_actor (str)
    '''
    
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
    '''Retorna el nombre del director y varios detalles del exito en sus peliculas.
    
    Args:
        nombre_director (str)
    '''
    
    nombre_director = nombre_director.lower()
    if nombre_director in df_credits_crew['crew_name_directing'].values:
        df_filtered = df_credits_crew[df_credits_crew['crew_name_directing'] == nombre_director]
        nombre = df_credits_crew[df_credits_crew['crew_name_directing'] == nombre_director]['crew_name_directing'].iloc[0]  
        peliculas_director = {}
        for index, row in df_filtered.iterrows():
            detalles_pelicula = {
                'Año': row['release_year'],
                'Retorno':  row['return'],
                'Costo': row['budget'],
                'Ganancia': row['revenue']  
            }
            peliculas_director[row['title']] = detalles_pelicula
        return {'message': f'El director {nombre} ha participado en las peliculas {peliculas_director}.'}
    else:
        return {'error': 'Nombre del director no valido. Por favor ingrese un nombre valido'}
    

@lru_cache(maxsize=128)  # Decorador para caché de resultados
@app.get('/Sistema_recomendacion/{titulo}')
def recomendacion(titulo: str):
    '''Retorna las 5 películas relacionadas con el título.'''
    
    titulo = titulo.lower()
    
    # Comprobación de existencia de la película
    if titulo in df_movies['title'].str.lower().values:
        pelicula = df_movies[df_movies['title'].str.lower() == titulo]

        if not pelicula.empty:
            pelicula_index = pelicula.index[0]
            features = np.column_stack([title_tfidf_reduced, company_tfidf_reduced, df_movies['popularity'].values])
            similarity_matrix = cosine_similarity(features)

            pelicula_similarities = similarity_matrix[pelicula_index]
            most_similar_pelicula_indices = np.argsort(-pelicula_similarities)

            most_similar_products_indices = most_similar_pelicula_indices[most_similar_pelicula_indices != pelicula_index]

            top_5_similar_products = df_movies.loc[most_similar_products_indices[:5], 'title'].tolist()

            return {"message": f"Las 5 películas más similares a {titulo} son: {top_5_similar_products}"}

    return {"error": "Película no encontrada"}
