# run application with gunicorn server (synchronous version) - for real life usage (prod)
# Light weight Linux version - not much software needs to run the application
FROM python:3.7.7-alpine3.12

RUN mkdir -p /home/PyMovieList/flaskMovieList

WORKDIR /home/PyMovieList/flaskMovieList

RUN pip install --upgrade pip

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

# add web server gunicorn to run application
RUN pip install gunicorn

COPY  ./flaskMovieList .

RUN chmod -R 777 .

ENV FLASK_APP=flaskMovieList_app.py

EXPOSE 5000

# start application
CMD gunicorn \
  --workers 4 \
  --threads 16 \
  --bind 0.0.0.0:5000 \
  flaskMovieList_app:app

