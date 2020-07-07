"""
    Module responsible for reload data from GHIBLI_API every 1 minute (Config.DATA_RELOAD_TIME)
    in background mode, in order to has better performance for sending data/page to user

    all data stored as static global variables
"""

import threading
import requests
import time

from .config import Config
from app import app, clear_cash
from typing import Dict

# is any data available to send back to user
result = False
# call back / waiter for getting data (firs time only)
result_available = threading.Event()
# thread responsible for refreshing data in background
data_load_thread = None

# data for movies and people for external usage by view
# key - movie id, value - movie
movies_data: Dict = {}
# key - people id, value - people
people_data: Dict = {}


def get_data() -> None:
    """
        Initial start of fetching data from  GHIBLI_API - just to setup background thread

        :return: None
    """
    app.logger.info(f'PyFlaskAlgorithmsAPI - {__name__} - get_data')
    global data_load_thread
    global result
    if not data_load_thread:
        app.logger.info(f'PyFlaskAlgorithmsAPI - {__name__} - get_data - create data_load_thread')
        data_load_thread = threading.Thread(target=load_data_from_api)
        data_load_thread.start()

        # wait here for the result to be available before continuing - first time only
        result_available.wait()


def load_data_from_api() -> None:
    """
        Fetch data from remote API - GHIBLI_API in background,
        parse and update existing data values after
        It runs with data_load_thread

        :return: None
    """
    global result
    app.logger.info(f'PyFlaskAlgorithmsAPI - {__name__} - load_data_from_api')
    try:
        request_movie_list = requests.get(url=Config.GHIBLI_API_ENDPOINT_FILMS)
        request_people_list = requests.get(url=Config.GHIBLI_API_ENDPOINT_PEOPLE)

        # get json/object from response
        result_movies = request_movie_list.json()
        result_people = request_people_list.json()

    except Exception as error:
        # in case of error (request issue or data corrupted) - skip this refresh phase, retry will be done
        # with data_load_thread the data my be not up to date from this point,
        # but at least the still should be something to
        # show (data from previous result) to end-user instead od error
        app.logger.error(f"The current request to {Config.GHIBLI_API_ENDPOINT_FILMS} cant be processed because {error}")

    else:
        # in case no any problems happened - parse and update existing data values
        update_data(result_movies, result_people)

    if not result:
        # attempt to retry load data again
        app.logger.info(f'PyFlaskAlgorithmsAPI - {__name__} - load_data_from_api - Retry')
        load_data_from_api()
    else:
        # refresh / reload data after 1 minute (Config.DATA_RELOAD_TIME)
        app.logger.info(f'PyFlaskAlgorithmsAPI - {__name__} - load_data_from_api - Done')
        time.sleep(Config.DATA_RELOAD_TIME)
        load_data_from_api()


def update_data(movies_json: Dict, people_json: Dict) -> None:
    """
         Parse and update existing data values for static / global
         movies_data and people_data

        :param movies_json: new data for movie List
        :param people_json: new data for people List

        :return: None
    """
    global result
    global movies_data
    global people_data

    movies_data_local = {}
    people_data_local = {}

    # create dictionary from people list
    for people in people_json:
        people_data_local[people["id"]] = people

    # create dictionary from movie list
    for movie in movies_json:
        movies_data_local[movie["id"]] = movie
        # keep all people related to a movie
        movie["people"] = []

    # map people to movie and movie to people
    for people in people_data_local.values():
        films = []
        for film in people["films"]:
            film_id = movie_id_from_url(film["url"])
            if film_id and movies_data_local[film_id]:
                films.append(movies_data_local[film_id])
                movies_data_local[film_id]["people"].append(people)
        people["films"] = films


    # it not consistent from source API side
    # for movie in movies_data.values():
    #     people_ar = []
    #     for people in movie["people"]:
    #         people_id = people_id_from_url(people["url"])
    #         if people_id and people_data[people_id]:
    #             people_ar.append(people_data[people_id])
    #     movie["people"] = people_ar

    # update both data holders will be atomic (both will be changed simultaneously)
    movies_data, people_data = movies_data_local, people_data_local

    result = True
    global result_available
    # notify get_data for case of first data loading
    result_available.set()
    # clear cash for all static pages in order to refresh static content with new data
    clear_cash()


def people_id_from_url(url: str) -> str:
    """
        Extract people id from people url

        :param url: people url from GHIBLI_API
        :return: people id
    """
    return url[len(Config.GHIBLI_API_ENDPOINT_PEOPLE) + 1:]


def movie_id_from_url(url: str) -> str:
    """
        Extract movie id from movie url

        :param url: movie url from GHIBLI_API
        :return: movie id
    """
    return url[len(Config.GHIBLI_API_ENDPOINT_FILMS) + 1:]
