import sqlite3

from dotenv import dotenv_values
from flask import Flask, render_template

config = dotenv_values(".env")
DB_LOCATION = config["DB_LOCATION"]

monitor = Flask(__name__)


@monitor.route('/')
def index():
    return render_template('index.html')


@monitor.route('/profiles')
def profiles():
    with sqlite3.connect(DB_LOCATION) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT username, full_name FROM profiles")
        profile_rows = cursor.fetchall()
    return render_template('profiles.html', profile_rows=profile_rows)


@monitor.route('/profile_followers/<int:userid>')
def profile_followers(userid: int):
    with sqlite3.connect(DB_LOCATION) as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT username, full_name FROM profiles "
                       f"INNER JOIN followers ON profiles.userid=followers.follower_id "
                       f"WHERE followers.userid={userid}")
        profile_rows = cursor.fetchall()
    return render_template("profiles.html", profile_rows=profile_rows)


if __name__ == "__main__":
    monitor.run(host='0.0.0.0')
