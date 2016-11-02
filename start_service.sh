#!/bin/bash
PORT=${1:-8003}
cd devenv/register_service
python run.py --port $PORT
cd ../..

if [ -d "/outter/static/" ]; then
	if [ -d "/outter/static/gaia_static" ]; then
		rm -rf /outter/static/gaia_static
	fi
	cp -rf static /outter/static/gaia_static/
fi

if [ "$_WEIZOOM_PRODUCTION" == "1" ]; then
	uwsgi service.ini
else
	python manage.py runserver 0.0.0.0 $PORT
fi
