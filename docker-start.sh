#!/bin/bash
WORKERS=$(( 2 * `cat /proc/cpuinfo | grep 'core id' | wc -l` + 1 ))
echo "Gunicorn workers: ${WORKERS}"

if [ ! -z ${WSGI_DEBUG} ]; then
	GUNICORN_LOG="--log-level DEBUG"
fi
echo "Checking required ENV variables"
declare -a envlist=("DB_USER" "DB_PASS" "DB_HOST" "EMAIL_USER" "EMAIL_PASSWORD")
for val in "${envlist[@]}"
do
  if [ -v ${!val} ]; then
     echo "- $val=not defined!"
  else
     echo "- $val=****"
  fi
done

exec gunicorn -w ${WORKERS} -b 0.0.0.0:8000 ${GUNICORN_LOG} --enable-stdio-inheritance pandas:app
