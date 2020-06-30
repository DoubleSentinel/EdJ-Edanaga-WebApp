FROM python:3.8.3-buster

WORKDIR /opt/source-code

COPY ./ ./

# find a way to pull latest unity release from other repo

EXPOSE 5000

CMD python -m http.server 5000
