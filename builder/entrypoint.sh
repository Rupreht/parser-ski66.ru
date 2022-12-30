#!/bin/sh

export STATIC_URL=/static
export STATIC_PATH=/app/app/static

crond -l 2 -f >/dev/stdout 2>/dev/stderr &
uwsgi --http 0.0.0.0:5000 --wsgi-file WSGI.py --callable app --stats 0.0.0.0:5001

# cd /app && python src/bot.py
