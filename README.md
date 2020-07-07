# PyMovieList
Python application which serves a page with Movie List of Studio Ghibli.


## Project setup steps (with Docker)

    1. Be sure your system has docker installed and your user has all required permissions to perform
    followed action

    2. Go to project root

        >  cd   your_local_directory/PyMovieList

    3. Build docker image, by default it take Dockerfile from current directory for build
        Depends on what service environment you want to use:

        > sudo docker build -t py-movie-list-image .
        or
        > sudo docker build -t py-movie-list-image-dev -f dev.Dockerfile .
        or
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