import logging
import sqlite3
from datetime import datetime

from dotenv import dotenv_values
from instaloader import Profile, Post, InstaloaderContext

config = dotenv_values("../.env")
DB_LOCATION = config["DB_LOCATION"]

logging.basicConfig(level=logging.DEBUG)


def update_followers(profile: Profile):
    """
    Scrape profile followers and update db tables 'profiles' and 'followers'
    """
    # TODO: use batches to update
    # TODO: check for existing db records and remove followers from db if they do not exist
    with sqlite3.connect(DB_LOCATION) as conn:
        cursor = conn.cursor()
        # add user profile to profiles
        sql_main_user = "REPLACE INTO profiles (userid, username, full_name)" \
                        "VALUES (?, ?, ?);"
        row = (profile.userid, profile.username, profile.full_name)
        cursor.execute(sql_main_user, row)

        # remove existing records because we are going to collect them again
        cursor.execute(f"DELETE FROM followers WHERE userid = {profile.userid}")

        # fill profiles table with follower profiles
        # and fill followers table with profiles relations
        sql_profiles = "REPLACE INTO profiles (userid, username, full_name) " \
                       "VALUES (?, ?, ?);"
        sql_followers = "REPLACE INTO followers (userid, follower_id) " \
                        "VALUES (?, ?);"

        for follower in profile.get_followers():
            logging.debug(f"Scraped {profile.username}'s follower {follower.username}")
            # update profiles table
            row_profiles = (follower.userid, follower.username, follower.full_name)
            cursor.execute(sql_profiles, row_profiles)

            # update followers table
            row_followers = (profile.userid, follower.userid)
            cursor.execute(sql_followers, row_followers)
    logging.info("Tables 'profiles' and 'followers' are updated")


def update_followings(profile: Profile):
    # TODO: use batches to update
    """
    Scrape profile followings (profiles that are followed by profile) and update db
    :param profile: instaloader.Profile - whose followings to scrape
    :return:
    """
    with sqlite3.connect(DB_LOCATION) as conn:
        cursor = conn.cursor()
        # add user profile to profiles
        sql_main_user = "REPLACE INTO profiles (userid, username, full_name)" \
                        "VALUES (?, ?, ?);"
        row = (profile.userid, profile.username, profile.full_name)
        cursor.execute(sql_main_user, row)

        sql_profiles = "REPLACE INTO profiles (userid, username, full_name) " \
                       "VALUES (?, ?, ?);"
        sql_followers = "REPLACE INTO followers (userid, follower_id) " \
                        "VALUES (?, ?);"
        for following in profile.get_followees():
            logging.debug(f"Scraped {profile.username}'s following {following.username}")
            # update profiles table
            row_profiles = (following.userid, following.username, following.full_name)
            cursor.execute(sql_profiles, row_profiles)

            # update followers table
            row_followers = (following.userid, profile.userid)
            cursor.execute(sql_followers, row_followers)
    logging.info("Tables 'profiles' and 'followers' are updated")


def update_posts(profile: Profile, limit: int = 10):
    """
    Scrape last posts (limited by 'limit') and put into db table 'posts'
    """
    sql = "REPLACE INTO posts (mediaid, userid) VALUES (?, ?);"
    with sqlite3.connect(DB_LOCATION) as conn:
        cursor = conn.cursor()
        for i, post in enumerate(profile.get_posts()):
            logging.debug(f"Scraped {profile.username}'s post with id {post.mediaid}")
            if i >= limit:
                break
            cursor.execute(sql, (post.mediaid, profile.userid))
    logging.info("Table 'posts' is updated")


def update_likes(post: Post):
    """
    Scrape profiles who likes given post and put to db
    :param post: instaloader.Post instance
    :return: None
    """
    # TODO: use batches to update
    sql = "INSERT INTO likes (mediaid, userid, scrape_datetime) VALUES (?, ?, ?);"
    with sqlite3.connect(DB_LOCATION) as conn:
        cursor = conn.cursor()
        likes = post.get_likes()
        for like in likes:
            logging.debug(f"Scraped like from {like.username} for {post.profile}'s "
                          f"post with id {post.mediaid}")
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            cursor.execute(sql, (post.mediaid, like.userid, date))
    logging.info("Table 'likes' is updated")


def update_likes_all_posts(context: InstaloaderContext):
    """
    Run 'update_post_likes' for all posts in db
    :return: None
    """
    sql = "SELECT mediaid FROM posts"
    with sqlite3.connect(DB_LOCATION) as conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        media_ids = cursor.fetchall()
    for mediaid in media_ids:
        post = Post.from_mediaid(context, mediaid[0])
        update_likes(post)
