import threading
import requests
from collections import defaultdict


result = False
result_available = threading.Event()
result_movies = {}
result_people = {}

# api-endpoint
URL = "https://ghibliapi.herokuapp.com/films"
URL_2 = "https://ghibliapi.herokuapp.com/people/"


def load_movie_list():
    request_movie_list = requests.get(url=URL)
    request_people_list = requests.get(url=URL_2)
    global result
    global result_movies
    global result_people

    result_movies = {}
    result_people = {}

    for people in request_people_list.json():
        result_people[people["id"]] = people

    for movie in request_movie_list.json():
        result_movies[movie["id"]] = movie

    for people in result_people.items():
        films = []
        for film in people["films"]:
            film_id = movie_id_from_url(film)
            if film_id and result_movies[film_id]:
                films.append(result_movies[film_id])
        people["films"] = films

    for movie in result_movies.items():
        people_ar = []
        for people in movie["people"]:
            people_id = people_id_from_url(people)
            if people_id and result_people[people_id]:
                people_ar.append(result_people[film_id])
        movie["people"] = people_ar

    result = True


def people_id_from_url(url):
    return url[39:]


def movie_id_from_url(url):
    return url[38:]
