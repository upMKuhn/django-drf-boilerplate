#!/bin/sh
set -xe

if [ "$1" = "--skip-migrations" ]; then
  shift
else
  DIR=`pwd`
  cd /app/
  python manage.py migrate --noinput
  python3 manage.py collectstatic --noinput
  cd $DIR
fi

# first arg is `-f` or `--some-option`
if [ "${1#-}" != "$1" ] || [ -z "$1" ]; then
	set -- uwsgi --ini /app/docker-provision/uwsgi.ini "$@"
fi

exec "$@"
