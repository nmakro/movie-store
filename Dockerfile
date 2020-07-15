FROM  python:3.8

RUN mkdir /home/movie-store

WORKDIR /home/movie-store

COPY requirements.txt requirements.txt


RUN python -m venv venv
RUN venv/bin/pip install --upgrade pip
RUN venv/bin/pip install -r requirements.txt

COPY app app

COPY moviestore.py start.sh ./

RUN chmod +x start.sh

ENV FLASK_APP moviestore.py

EXPOSE 5000

ENTRYPOINT ["./start.sh"]