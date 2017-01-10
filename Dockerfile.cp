FROM alpine:latest
#FROM python:3-onbuild
#FROM httpd:2.4

MAINTAINER Artem Goncharov

#RUN apt-get install python3 libapache2-mod-wsgi && \
#    python3 -m ensurepip && \
#    rm -r /usr/lib/python*/ensurepip && \
#    pip3 install --upgrade pip setuptools && \
#    rm -r /root/.cache

# Update
RUN apk add --update python3 apache2 apache2-mod-wsgi \
	# fix "httpd: Could not reliably determine the server's fully qualified domain name" error \
    && sed -i '1s/^/ServerName localhost \n\n/' /etc/apache2/httpd.conf \
    && mkdir /run/apache2

COPY ./requirements.txt /tmp

# Install app dependencies
RUN pip3 install -r /tmp/requirements.txt

COPY . /var/www/homeautomation
COPY ./homeautomation_vhost.conf /etc/apache2/conf.d

EXPOSE 8008

#ENTRYPOINT ["/usr/sbin/httpd"] 
#CMD ["-D", "FOREGROUND"]

#CMD ["python3", "/var/www/homeautomation/run.py"]