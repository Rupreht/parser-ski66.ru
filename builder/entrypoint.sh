#!/bin/sh

export STATIC_URL=/static
export STATIC_PATH=/app/app/static

crond -l 2 -f >/proc/self/fd/1 2>/proc/self/fd/2 &
uwsgi --http 0.0.0.0:5000 --wsgi-file WSGI.py --callable app --uid app --gid app --processes 4 --threads 2 --stats 0.0.0.0:5001
