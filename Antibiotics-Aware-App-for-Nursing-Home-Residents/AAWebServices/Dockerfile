FROM python:2.7-wheezy
MAINTAINER Wooyong Ee <wee3@gatech.edu>

COPY . /usr/src/app
WORKDIR /usr/src/app

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=.:/usr/src/app
EXPOSE 5000
CMD cd /usr/src/app && python api.py