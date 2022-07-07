#!/bin/sh

crond -l 2 -f >/dev/stdout 2>/dev/stderr &
cd /app && python src/bot.py
