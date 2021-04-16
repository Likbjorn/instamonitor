from dotenv import dotenv_values
from instaloader import Instaloader, Profile

from scraper.update_db import update_followers, update_posts, update_likes_all_posts, update_followings

config = dotenv_values("../.env.private")
LOGIN = config["LOGIN"]
PASSWORD = config["PASSWORD"]

if __name__ == "__main__":
    username = 'mishugina_art'
    loader = Instaloader()
    loader.login(LOGIN, PASSWORD)
    profile = Profile.from_username(username=username, context=loader.context)
    update_followers(profile)
    update_followings(profile)
    update_posts(profile)
    update_likes_all_posts(loader.context)
