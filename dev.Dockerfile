# run application as stand alon server - for development needs only
# Light weight Linux version - not much software needs to run the application
FROM python:3.7.7-alpine3.12

RUN mkdir -p /home/PyMovieList/flaskMovieList

WORKDIR /home/PyMovieList/flaskMovieList

RUN pip install --upgrade pip

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY  ./flaskMovieList .

EXPOSE 5000

ENTRYPOINT [ "python" ]

CMD [ "flaskMovieList_app.py" ]



