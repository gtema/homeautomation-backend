FROM python:3.6-alpine

LABEL version="1.0"
LABEL description="The backend of my Homeautomatizaion"

EXPOSE 5000

WORKDIR /code

# install postgresql
RUN apk update && \
    apk add --virtual build-deps gcc python-dev musl-dev && \
    apk add postgresql-dev

# env var for further reference
ENV REQ_FILE=requirements.txt

# copy requirements file
COPY ${REQ_FILE} /code
RUN pip install -r ${REQ_FILE}

ADD . /code
# compile files
RUN python -m compileall .

CMD ["python", "run.py"]
