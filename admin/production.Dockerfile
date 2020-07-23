FROM python:3.8.3-buster

WORKDIR /opt/source-code

# first import dependencies on this layer to optimize layering
COPY ./Pipfile* ./

RUN pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile 

COPY ./app ./

EXPOSE 5000

CMD uwsgi --http-socket :5000 --wsgi-file app.py
