"""
    flask application configuration variables
"""

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """
        Class with configurations
    """
    API_URL = ""

    DEBUG_GLOBAL = True

    # default host ip
    HOST_API_APP = "0.0.0.0"

    # wep app port
    PORT_API_APP = "5000"

    # api root url
    SERVER_NAME_API_APP = "/algorithms/api/v1"

    # log location
    LOG_DIRRECTORY = "logs/movieList.log"
    LOG_SIZE = 10240
    LOG_BACKUP_COUNT = 10


    # to avoid creation of logging and monitoring dashboard for tests
    TESTING = False

    # api-endpoint
    GHIBLI_API_ENDPOINT_FILMS = "https://ghibliapi.herokuapp.com/films/"
    GHIBLI_API_ENDPOINT_PEOPLE = "https://ghibliapi.herokuapp.com/people/"
