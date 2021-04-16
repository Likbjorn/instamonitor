FROM python:3.7

ENV CELERY_BROKER_URL redis://redis:6379/0
ENV CELERY_RESULT_BACKEND redis://redis:6379/0
ENV C_FORCE_ROOT true
ENV PYTHONUNBUFFERED 1
ENV DB_LOCATION "/db/instagram.db"

COPY ./requirements.txt /scraper/requirements.txt
RUN pip install -r /scraper/requirements.txt
COPY . /scraper
WORKDIR /scraper

# RUN python init_database.py -e DB_LOCATION=$DB_LOCATION

# TODO: run init_databese.py separately
ENTRYPOINT python init_database.py && celery -A celery_tryout worker --loglevel=info