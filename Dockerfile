#FROM alpine:3.5
FROM python:3-onbuild

# Update
#RUN apk add --update python3 py-pip

#COPY server/requirements.txt /src/requirements.txt

# Install app dependencies
#RUN pip install -r /src/requirements.txt

# Bundle app source
#COPY server/run.py /src/server.py

EXPOSE  5000
CMD ["python", "./run.py", "-p 5000"]