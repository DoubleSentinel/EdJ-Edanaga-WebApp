FROM python:3.8.3-buster

WORKDIR /opt/source-code

COPY ./ ./

RUN pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile 

EXPOSE 5000

CMD uwsgi --http-socket :5000 --wsgi-file app.py
