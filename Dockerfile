FROM python:3.9-alpine
WORKDIR /usr/src/reapr
COPY requirements.yml .
RUN pip install -r requirements.yml
RUN apk update && apk add tzdata 
ENV TZ="America/Boise"
