"""
    Standard Flask routing - just simple url to function mapping
"""

from flask import render_template, abort, redirect, url_for
from app import app, movieListLoader, cache
from functools import wraps
from app.config import Config


def load_data(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        movieListLoader.get_data()
        if not movieListLoader.result:
            abort(404, description=f"GHIBLI API_ENDPOINTS ARE NOT AVAILABLE")
        return func(*args, **kwargs)
    return decorated


def validate_details_data(data_dic, id, name):
    if id not in data_dic:
        abort(404, description=f"The {name} with id={id} not found")
    return data_dic[id]


@cache.cached(timeout=0)
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
@cache.cached(timeout=0)
def index():
    """
        Welcome page
    :return: page itself
    """
    return render_template('index.html', title='Welcome here')


@app.route('/movies')
@app.route('/movies/')
@load_data
@cache.cached()
def movies():
    """
        Welcome page
    :return: page itself
    """

    return render_template('movieList.html',
                           title='Movie List',
                           headers=["Title", "Date", "Description", "People"],
                           movie_list=movieListLoader.movies_data)

@app.route('/movies/<movie_id>')
@load_data
@cache.cached()
def movies_details(movie_id):
    """
        Welcome page
    :return: page itself
    """
    if not movie_id:
        return redirect(url_for('movies'))

    movie = validate_details_data(movieListLoader.movies_data, movie_id, "movie")
    return render_template('details.html',
                           title=f'Movie Details - {movie["title"]}',
                           fields=["id", "title", "description", "producer", "release_date", "people"],
                           data=movie)


@app.route('/people')
@app.route('/people/')
@load_data
@cache.cached()
def people():
    """
        Welcome page
    :return: page itself
    """

    return render_template('peopleList.html',
                           title='People List',
                           headers=["Name", "Gender", "Age", "Films"],
                           people_list=movieListLoader.people_data)


@app.route('/people/<people_id>')
@load_data
@cache.cached()
def people_details(people_id):
    """
        Welcome page
    :return: page itself
    """
    if not people_id:
        return redirect(url_for('people'))

    people = validate_details_data(movieListLoader.people_data, people_id, "people")
    return render_template('details.html',
                           title=f'People Details - {people["name"]}',
                           fields=["id", "name", "gender", "age", "eye_color", "hair_color", "films"],
                           data=people)
