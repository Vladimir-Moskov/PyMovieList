# PyMovieList
Python application which serves a page with Movie List of Studio Ghibli.

## Here is solution
I have been used "old good" monolith approach for application architecture
(no needs in microservices and decomposition for current requirements)

  0. Please, see Task statement in "Backend coding challenge_sennder_New.txt"
  1. Flask framework has been used to implement task as web application.
  2. Web app source code in PyMovieList/flaskMovieList/ directory
  3. Unit/International tests  in PPyMovieList/flaskMovieList/tests/ directory.
  6. Simple (Flask build in) cache has been implemented to return "static" content

## From point of view MVP (Minimum Valuable Product)

1. For simplicity - only basic logging has been added

2. For simplicity - unit tests and integration tests has not been implemented on 100%, only simple test cases

3. For simplicity - there is no any authorization/security
> TODO: implement it

4. Error handling have not been done on full scale
> TODO: implement it

## Project setup steps (with Docker)

    1. Be sure your system has docker installed and your user has all required permissions to perform
    followed action

    2. Go to project root

        >  cd   your_local_directory/PyMovieList

    3. Build docker image, by default it take Dockerfile from current directory for build
        Depends on what service environment you want to use:

        for 'production' case
        > sudo docker build -t py-movie-list-image .

        or
        for developer environment only
        > sudo docker build -t py-movie-list-image-dev -f dev.Dockerfile .

        or  for 'production' case with async service container
        > sudo docker build -t py-movie-list-image-async -f async-gevent.Dockerfile .

    4. Run docker image with web api application running on it
        Depends on what service environment you want to use:
        > sudo docker run --init --rm --publish 5000:5000 py-movie-list-image
        or
        > docker run --init --rm --publish 5000:5000 py-movie-list-image-dev
        or
        > docker run --init --rm --publish 5000:5000 py-movie-list-image-async


        > docker run --name py-movie-list-image -d -p 5000:5000 --rm py-movie-list-image

    5. In case permission issue - your user not in sudo group, run previous commands without sudo


## Project setup steps (on OS directly / development Environment)

 1. download / unzip project into your local disc, be sure project in PyMovieList directory

 2. Install latest Python 3.7 if you do not have [https://realpython.com/installing-python/]
    and run cmd / terminal console

 3. Install pip  use command
   > python get-pip.py
   or follow step by step [https://www.liquidweb.com/kb/install-pip-windows/]

 4. Install Python virtualenv with command
   > pip install virtualenv

 5. set project folder as you current folder
    > cd   your_local_directory/PyMovieList

 6. Run next command in order to create virtualenv for project
   > virtualenv venv

 7. Activate virtual environment
   > ./venv/Scripts/activate

 8. install project dependencies
    return to project root
   > cd your_local_directory/PyMovieList

   > pip install -r requirements.txt

    and use

    > pip freeze > requirements.txt

    in order to update list of project libraries
    and use

    > pip install <package-name>

    in case you miss some


 ### Start web api application

    1.  Here is where application located -
        > PyMovieList/flaskMovieList/flaskMovieList_app.py

    2. Run it with
       >  python PyMovieList/flaskMovieList/flaskMovieList_app.py
       or just
       >  python flaskMovieList/flaskMovieList_app.py

    3. application will be started on default HOST and PORT

        > http://localhost:5000/

    4. The flowing API endpoints will be exposed to execute corespondent algorithms:
        (ip may be different - 127.0.0.1, localhost, depends where you deploy and how you asses web API)

         ### The web application has next available pages:
            * http://127.0.0.1:5000/
            * http://127.0.0.1:5000/movies/
            * http://127.0.0.1:5000/people/
            * http://127.0.0.1:5000/movies/<movie_id>
            * http://127.0.0.1:5000/people/<people_id>


