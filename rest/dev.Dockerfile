FROM python:3.8.3-buster

WORKDIR /tmp

COPY ./Pipfile* ./

RUN pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile 

EXPOSE 5000

WORKDIR /opt/source-code

ENV FLASK_ENV=development

CMD flask run --host 0.0.0.0
