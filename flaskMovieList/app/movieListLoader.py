import threading
import requests
import time

from .config import Config
from app import app, clear_cash
from typing import Dict

result = False
result_available = threading.Event()
data_load_thread = None

movies_data = {}
people_data = {}


def get_data():
    app.logger.info(f'PyFlaskAlgorithmsAPI - {__name__} - get_data')
    global data_load_thread
    global result
    if not data_load_thread:
        app.logger.info(f'PyFlaskAlgorithmsAPI - {__name__} - get_data - create data_load_thread')
        thread = threading.Thread(target=load_data_from_api)
        thread.start()

        # wait here for the result to be available before continuing
        result_available.wait()


def load_data_from_api():
    global result
    app.logger.info(f'PyFlaskAlgorithmsAPI - {__name__} - load_data_from_api')
    try:
        request_movie_list = requests.get(url=Config.GHIBLI_API_ENDPOINT_FILMS)
        request_people_list = requests.get(url=Config.GHIBLI_API_ENDPOINT_PEOPLE)
        result_movies = request_movie_list.json()
        result_people = request_people_list.json()

    except Exception as error:
        app.logger.error(f"The current services cant be processed because {error}")


        global movies_data
        global people_data
        movies_data = {}
        people_data = {}
        result = False
    else:
        update_data(result_movies, result_people)

    if not result:
        # attempt to retry load data again
        app.logger.info(f'PyFlaskAlgorithmsAPI - {__name__} - load_data_from_api - Retry')
        load_data_from_api()
    else:
        app.logger.info(f'PyFlaskAlgorithmsAPI - {__name__} - load_data_from_api - Done')
        time.sleep(Config.DATA_RELOAD_TIME)
        load_data_from_api()


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
        #
        movie["people"] = []

    for people in people_data.values():
        films = []
        for film in people["films"]:
            film_id = movie_id_from_url(film)
            if film_id and movies_data[film_id]:
                films.append(movies_data[film_id])
                movies_data[film_id]["people"].append(people)
        people["films"] = films


    # it not consistent from source API side
    # for movie in movies_data.values():
    #     people_ar = []
    #     for people in movie["people"]:
    #         people_id = people_id_from_url(people)
    #         if people_id and people_data[people_id]:
    #             people_ar.append(people_data[people_id])
    #     movie["people"] = people_ar

    result = True
    global result_available
    result_available.set()
    clear_cash()


def people_id_from_url(url):
    return url[len(Config.GHIBLI_API_ENDPOINT_PEOPLE):]


def movie_id_from_url(url):
    return url[len(Config.GHIBLI_API_ENDPOINT_FILMS):]
