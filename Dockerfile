FROM python:3.6-alpine

MAINTAINER Artem Goncharov

EXPOSE 5000

ADD . /code

WORKDIR /code

RUN pip install -r requirements_nopg.txt

CMD ["python", "run.py"]
