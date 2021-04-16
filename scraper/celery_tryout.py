import os
import logging
from celery import Celery

CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL',
                                   'redis://localhost:6379'),
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND',
                                       'redis://localhost:6379')

scraper = Celery('tasks',
                 broker=CELERY_BROKER_URL,
                 backend=CELERY_RESULT_BACKEND)


@scraper.task()
def hello_celery():
    logging.info("Hello celery")


if __name__ == "__main__":
    hello_celery.delay()
