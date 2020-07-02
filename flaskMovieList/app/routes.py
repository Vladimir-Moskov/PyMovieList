"""
    Standard Flask routing - just simple url to function mapping
"""

from flask import render_template, abort
from app import app, movieListLoader
from functools import wraps


def load_data(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        if not movieListLoader.result:
            movieListLoader.load_movie_list()
        return func(*args, **kwargs)
    return decorated


def validate_details_data(data_dic, id, name):
    if not data_dic[id]:
        abort(404, description=f"The {name} with id={id} not found")
    return data_dic[id]



@app.errorhandler(404)
def not_found(e):
    """
         use template made by Colorlib (https://colorlib.com)
    :param e: request
    :return: error page wrapper
    """
    return render_template('404.html'), 404


@app.route('/')
@app.route('/index')
@load_data
def index():
    """
        Welcome page
    :return: page itself
    """
    return render_template('index.html', title='Welcome here')


@load_data
@app.route('/movies')
def movies():
    """
        Welcome page
    :return: page itself
    """

    return render_template('movieList.html',
                           title='Movie List',
                           headers=["Title"],
                           movie_list=movieListLoader.result_movies)

@load_data
@app.route('/movies/<movie_id>')
def movies_details(movie_id):
    """
        Welcome page
    :return: page itself
    """
    movie = validate_details_data(movieListLoader.result_movies, movie_id, "movie")
    return render_template('details.html',
                           title='Movie Details',
                           fields=["id", "title", "description", "producer", "release_date", "people"],
                           data=movie)


@load_data
@app.route('/people')
def people():
    """
        Welcome page
    :return: page itself
    """

    return render_template('peopleList.html',
                           title='People List',
                           headers=["Name"],
                           people_list=movieListLoader.result_people)

@load_data
@app.route('/movies/<people_id>')
def people_details(people_id):
    """
        Welcome page
    :return: page itself
    """
    people = validate_details_data(movieListLoader.result_movies, people_id, "people")
    return render_template('details.html',
                           title='Movie Details',
                           fields=["id", "name", "gender", "age", "eye_color", "hair_color", "films"],
                           data=people)
