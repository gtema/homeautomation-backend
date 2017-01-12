FROM python:3.5-alpine

MAINTAINER Artem Goncharov

ADD . /code

WORKDIR /code

EXPOSE 5000

RUN pip install -r requirements.txt

CMD ["python", "run.py"]