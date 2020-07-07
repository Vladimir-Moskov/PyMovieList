"""
    Integration tests for every page of wep application routers

    for now, only simple-positive test cases has been implemented
"""

import pytest
from app import app, movieListLoader
from app.config import Config
from .resources import *

# set application in state for testing (turn off logging and monitoring dashboard)
Config.TESTING = True


@pytest.fixture()
def client():
    """
        Create "lambda service" / application to handle http request for test case

        :return: client - "lambda service" / application to handle http request
    """
    # setup mock data
    movieListLoader.result = True
    movieListLoader.data_load_thread = True
    movieListLoader.movies_data = test_movie_list
    movieListLoader.people_data = test_people_list

    with app.test_client() as client:
        yield client


@pytest.mark.parametrize("page", ['/',
                                  '/index',
                                  'movies/',
                                  'people/',
                                  f'movies/{test_movie_id}',
                                  f'people/{test_people_id}'])
def test_right_pages(client, page):
    """
        Simple check of pages availability for a site map

       :param client: app client
       :param page: current page
    """
    response = client.get(page, content_type='html/text')
    assert response.status_code, 200


@pytest.mark.parametrize("page", ['page', 'login'])
def test_wrong_pages(client, page):
    """
        Simple check of other pages 404

       :param client: app client
       :param page: current page
    """
    response = client.get(page, content_type='html/text')
    assert response.status_code, 404


def test_movie_on_movie_list_page(client):
    """
        Simple check if result movie list on the page

       :param client: app client
    """
    response = client.get('movies/', content_type='html/text')

    assert test_movie_list[test_movie_id]['title'] in response.data.decode('ascii')


def test_movie_on_movie_details_page(client):
    """
        Simple check if result movie on the page movie details

       :param client: app client
    """
    response = client.get(f'movies/{test_movie_id}', content_type='html/text')

    assert test_movie_id in response.data.decode('ascii')
    assert test_movie_list[test_movie_id]['title'] in response.data.decode('ascii')


def test_people_on_people_list_page(client):
    """
        Simple check if result people list on the page

       :param client: app client
    """
    response = client.get('people/', content_type='html/text')

    assert test_people_list[test_people_id]['name'] in response.data.decode('ascii')


def test_people_on_people_details_page(client):
    """
        Simple check if result people on the page people details

       :param client: app client
    """
    response = client.get(f'people/{test_people_id}', content_type='html/text')

    assert test_people_id in response.data.decode('ascii')
    assert test_people_list[test_people_id]['name'] in response.data.decode('ascii')
