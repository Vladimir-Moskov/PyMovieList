"""
    Tests for movieListLoader

    for now, only simple-positive test cases has been implemented
"""

from unittest import mock
from app.config import Config
from .resources import *
import app.movieListLoader as movieListLoader

# set application in state for testing (turn off logging and monitoring dashboard)
Config.TESTING = True


def mocked_requests_get(*args, **kwargs):
    """
        This method will be used by the mock to replace requests.get

        :param args: requests args
        :param kwargs: requests kwargs
        :return: response MockResponse
    """
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    test_movie_list_local = test_movie_list
    test_people_list_local = test_people_list
    test_movie_list_local[test_movie_id]["people"] = [test_people_list[test_people_id]["url"]]
    test_people_list_local[test_people_id]["films"] = [test_movie_list_local[test_movie_id]["url"]]

    if args:
        if args[0] == Config.GHIBLI_API_ENDPOINT_FILMS:
            return MockResponse([test_movie_list_local[test_movie_id]], 200)
        elif args[0] == Config.GHIBLI_API_ENDPOINT_PEOPLE:
            return MockResponse([test_people_list_local[test_people_id]], 200)
    if kwargs:
        if kwargs['url'] == Config.GHIBLI_API_ENDPOINT_FILMS:
            return MockResponse([test_movie_list_local[test_movie_id]], 200)
        elif kwargs['url'] == Config.GHIBLI_API_ENDPOINT_PEOPLE:
            return MockResponse([test_people_list_local[test_people_id]], 200)

    return MockResponse(None, 404)


def test_initial_sate():
    """
        Check initial state of movieListLoader
    """
    assert not movieListLoader.result
    assert not movieListLoader.people_data
    assert not movieListLoader.movies_data


@mock.patch('requests.get', side_effect=mocked_requests_get)
def test_get_data(mock_get):
    """
        Check state of movieListLoader after data loading
    """
    movieListLoader.get_data()
    assert movieListLoader.result
    assert movieListLoader.people_data
    assert movieListLoader.movies_data

    assert test_movie_id in movieListLoader.movies_data
    assert test_people_id in movieListLoader.people_data
    assert movieListLoader.people_data[test_people_id] in movieListLoader.movies_data[test_movie_id]["people"]
    assert movieListLoader.movies_data[test_movie_id] in movieListLoader.people_data[test_people_id]["films"]
