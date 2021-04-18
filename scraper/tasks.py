import os
from celery.utils.log import get_task_logger
from celery import Celery

CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL',
                                   'redis://localhost:6379/0'),
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND',
                                       'redis://localhost:6379/0')

scraper = Celery('tasks',
                 broker=CELERY_BROKER_URL,
                 backend=CELERY_RESULT_BACKEND)
logger = get_task_logger('tasks')

scraper.conf.beat_schedule = {
    'sample-task': {
        'task': 'tasks.hello_celery',
        'schedule': 10.0,
    },
}


@scraper.task()
def hello_celery():
    logger.info("Hello logger")
