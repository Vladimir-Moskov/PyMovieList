
"""
    Integration tests for every endpoint of Algorithms Wep API application

    for now, only simple-positive test cases has been implemented
"""
from app.config import Config
# set application in state for testing (turn off logging and monitoring dashboard)
Config.TESTING = True


import pytest
from app import app, movieListLoader
from pytest_mock import mocker

test_movie_list = {
"2baf70d1-42bb-4437-b551-e5fed5a87abe":
     {
        "id": "2baf70d1-42bb-4437-b551-e5fed5a87abe",
        "title": "Castle in the Sky",
        "description": "The orphan Sheeta inherited a mysterious crystal that links her to the mythical sky-kingdom of"
                       " Laputa. With the help of resourceful Pazu and a rollicking band of sky pirates, she makes"
                       " her way to the ruins of the once-great civilization. Sheeta and Pazu must outwit the evil"
                       " Muska, who plans to use Laputa's science to make himself ruler of the world.",
        "director": "Hayao Miyazaki",
        "producer": "Isao Takahata",
        "release_date": "1986",
        "rt_score": "95",
        "people": [
        ]
      }
}

test_people_list = {
    "ba924631-068e-4436-b6de-f3283fa848f0": {
        "id": "ba924631-068e-4436-b6de-f3283fa848f0",
        "name": "Ashitaka",
        "gender": "Male",
        "age": "late teens",
        "eye_color": "Brown",
        "hair_color": "Brown",
        "films": [
        ]
    }
}

@pytest.fixture()
def client():
    """
        Create "lambda service" / application to handle http request for test case

        :return: client - "lambda service" / application to handle http request
    """
    movieListLoader.result = True
    movieListLoader.data_load_thread = True
    movieListLoader.movies_data = test_movie_list
    movieListLoader.people_data = test_people_list

    with app.test_client() as client:
        yield client


@pytest.mark.parametrize("page", ['/', '/index', 'movies/', 'people/'])
def test_right_pages(client, page):
    response = client.get(page, content_type='html/text')
    assert response.status_code, 200


@pytest.mark.parametrize("page", ['page', 'login'])
def test_wrong_pages(client, page):
    response = client.get(page, content_type='html/text')
    assert response.status_code, 404