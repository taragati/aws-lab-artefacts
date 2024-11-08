# syntax=docker/dockerfile:1
FROM python:3.8

# Create app directory
RUN mkdir /app
WORKDIR /app

# Install app dependencies
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY service.py /app
COPY country-by-calling-code-v1.json /app

ENV FLASK_APP=service.py
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=80"]