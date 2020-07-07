import threading
import requests
from .config import Config
from app import app
from typing import Dict

result = False
result_available = threading.Event()


movies_data = {}
people_data = {}


def load_data_from_api():
    try:
        request_movie_list = requests.get(url=Config.GHIBLI_API_ENDPOINT_FILMS)
        request_people_list = requests.get(url=Config.GHIBLI_API_ENDPOINT_PEOPLE)
        result_movies = request_movie_list.json()
        result_people = request_people_list.json()

    except Exception as error:
        app.logger.error(f"The current services cant be processed because {error}")

        global result
        global movies_data
        global people_data
        movies_data = {}
        people_data = {}
        result = False
    else:
        update_data(result_movies, result_people)


def update_data(movies_json: Dict, people_json: Dict):
    global result
    global movies_data
    global people_data

    movies_data = {}
    people_data = {}

    for people in people_json:
        people_data[people["id"]] = people

    for movie in movies_json:
        movies_data[movie["id"]] = movie

    for people in people_data.values():
        films = []
        for film in people["films"]:
            film_id = movie_id_from_url(film)
            if film_id and movies_data[film_id]:
                films.append(movies_data[film_id])
        people["films"] = films

    for movie in movies_data.values():
        people_ar = []
        for people in movie["people"]:
            people_id = people_id_from_url(people)
            if people_id and people_data[people_id]:
                people_ar.append(people_data[people_id])
        movie["people"] = people_ar

    result = True


def people_id_from_url(url):
    return url[len(Config.GHIBLI_API_ENDPOINT_PEOPLE):]


def movie_id_from_url(url):
    return url[len(Config.GHIBLI_API_ENDPOINT_FILMS):]
