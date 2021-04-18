import os
from celery.utils.log import get_task_logger
from celery import Celery
from instaloader import Instaloader, Profile

import update_db as db

CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL',
                                   'redis://localhost:6379/0'),
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND',
                                       'redis://localhost:6379/0')
LOGIN = os.environ.get("LOGIN")
PASSWORD = os.environ.get("PASSWORD")

scraper = Celery('tasks',
                 broker=CELERY_BROKER_URL,
                 backend=CELERY_RESULT_BACKEND)
logger = get_task_logger('tasks')

scraper.conf.beat_schedule = {
    'update_followers': {
        'task': 'tasks.update_followers',
        'schedule': 600.0,
    },
    'update_followings': {
        'task': 'tasks.update_followings',
        'schedule': 600.0,
    },
    'update_likes': {
        'task': 'tasks.update_likes',
        'schedule': 600.0,
    },
    'update_posts': {
        'task': 'tasks.update_posts',
        'schedule': 600.0,
    },
}


@scraper.task()
def update_followers():
    logger.info("Start updating followers")
    username = 'mishugina_art'
    loader = Instaloader()
    loader.login(LOGIN, PASSWORD)
    profile = Profile.from_username(username=username, context=loader.context)
    db.update_followers(profile)


@scraper.task()
def update_followings():
    username = 'mishugina_art'
    loader = Instaloader()
    loader.login(LOGIN, PASSWORD)
    profile = Profile.from_username(username=username, context=loader.context)
    db.update_followings(profile)


@scraper.task()
def update_posts():
    username = 'mishugina_art'
    loader = Instaloader()
    loader.login(LOGIN, PASSWORD)
    profile = Profile.from_username(username=username, context=loader.context)
    db.update_posts(profile)


@scraper.task()
def update_likes():
    loader = Instaloader()
    loader.login(LOGIN, PASSWORD)
    db.update_likes_all_posts(loader.context)
