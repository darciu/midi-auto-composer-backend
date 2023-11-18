FROM python:3.9-slim

LABEL maintainer="giemzadariusz@gmail.com"\
    description="App serving midi files"


RUN apt-get update
RUN apt-get -y install fluidsynth
RUN apt-get -y install pkg-config
RUN apt-get -y install libasound2-dev
RUN apt-get -y install libjack-dev



RUN mkdir /code

COPY requirements.txt /code/

RUN pip3.9 install -r /code/requirements.txt

COPY ./ /code/

WORKDIR /code/

EXPOSE 8000

CMD uvicorn main:app --app-dir src/ --host 0.0.0.0 --port 8000 --reload