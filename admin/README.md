# Development Environment

_To run the admin application for development, run it with pipenv_

1. Install dependencies
`pipenv install`
2. Launch mongoDB
`docker run -p 27017-27019:27017-27019 -v /path/to/local/volume:/data/db mongo:latest --auth`
3. Run development environment
`pipenv run flask run`


# Deployment

_To run the admin application on deploy target_

1. Access the deployment server through SSH and clone this repo
2. Containerize with docker
   1. Ensure the Dockerfile is up to date
   2. Build the image with
      `docker build ./ -t edanaga/admin`
3. Instanciate container with
   `docker run --name edanaga_admin edanaga/admin`

