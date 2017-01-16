FROM python:3.5-alpine

MAINTAINER Artem Goncharov

EXPOSE 5000

ADD . /code

WORKDIR /code


RUN pip install -r requirements.txt

#ENTRYPOINT ["python"]

CMD ["python", "run.py"]