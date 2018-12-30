FROM python:3.6

ENV APP_HOME=/mappanddas-api
ENV PYTHONUNBUFFERED=1
RUN mkdir -p ${APP_HOME}
WORKDIR ${APP_HOME}

COPY Pipfile Pipfile.lock *.py docker-start.sh ${APP_HOME}/

RUN pip3 install pipenv&& \
    pipenv install --deploy --system

ENTRYPOINT ["./docker-start.sh"]
