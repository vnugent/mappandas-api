#!/bin/bash
WORKERS=$(( 2 * `cat /proc/cpuinfo | grep 'core id' | wc -l` + 1 ))
echo "Gunicorn workers: ${WORKERS}"

if [ ! -z ${WSGI_DEBUG} ]; then
	GUNICORN_LOG="--log-level DEBUG"
fi

exec gunicorn -w ${WORKERS} -b 0.0.0.0:8000 ${GUNICORN_LOG} --capture-output pandas:app