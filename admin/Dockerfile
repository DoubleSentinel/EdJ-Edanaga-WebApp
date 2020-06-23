FROM ubuntu

RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y python3-pip

RUN python3 -m pip install flask
RUN python3 -m pip install mongoengine
RUN python3 -m pip install flask-mongoengine
RUN python3 -m pip install email_validator
RUN python3 -m pip install flask-security
RUN python3 -m pip install flask-admin

EXPOSE 5000

COPY . /opt/source-code

ENV FLASK_APP=/opt/source-code/app.py

CMD flask run
