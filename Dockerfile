FROM grahamdumpleton/mod-wsgi-docker:python-3.5-onbuild

MAINTAINER Artem Goncharov

CMD ["api.wsgi"]