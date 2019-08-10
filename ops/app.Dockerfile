FROM python:3.7-alpine
ENV PYTHONPATH=$PATH:/app/src

RUN mkdir /app
WORKDIR /app

RUN apk add \
  python3-dev \
  build-base \
  linux-headers \
  pcre-dev \
  gcc \
  musl-dev \
  postgresql-dev


RUN pip install pipenv
COPY ./Pipfile ./Pipfile.lock ./
RUN pipenv install --system

ADD ./ .

COPY ./ops/docker-django-entrypoint.sh /usr/local/bin/docker-django-entrypoint
ENTRYPOINT ["/usr/local/bin/docker-django-entrypoint"]

# Socket
EXPOSE 8000
