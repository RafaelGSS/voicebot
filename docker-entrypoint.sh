#!/bin/bash
set -e

if [ ! -f .env ]; then
	env > .env
fi

exec uwsgi --ini conf/uwsgi.ini
