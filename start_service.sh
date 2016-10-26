#!/bin/bash
PORT=${1:-8003}
cd register_service
python register.py --port $PORT
cd ..
python manage.py runserver 0.0.0.0 $PORT
