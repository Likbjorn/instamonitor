import sqlite3

from dotenv import dotenv_values

config = dotenv_values(".env")
DB_LOCATION = config["DB_LOCATION"]

if __name__ == "__main__":
    # create db
    with sqlite3.connect(DB_LOCATION) as conn:
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.execute("CREATE TABLE IF NOT EXISTS profiles ("
                     "userid integer PRIMARY KEY,"
                     "username text NOT NULL,"
                     "full_name character);")
        conn.execute("CREATE TABLE IF NOT EXISTS posts ("
                     "mediaid integer PRIMARY KEY,"
                     "userid integer NOT NULL,"
                     "FOREIGN KEY (userid)"
                     "  REFERENCES profiles (userid)"
                     "    ON DELETE CASCADE);")
        conn.execute("CREATE TABLE IF NOT EXISTS likes ("
                     "mediaid integer NOT NULL,"
                     "userid integer NOT NULL,"
                     "scrape_datetime text,"
                     "UNIQUE (mediaid, userid) ON CONFLICT REPLACE,"
                     "FOREIGN KEY (mediaid)"
                     "  REFERENCES posts (mediaid)"
                     "    ON DELETE CASCADE,"
                     "FOREIGN KEY (userid)"
                     "  REFERENCES profiles (userid)"
                     "    ON DELETE CASCADE);")
        conn.execute("CREATE TABLE IF NOT EXISTS followers ("
                     "userid integer NOT NULL,"
                     "follower_id integer NOT NULL,"
                     "UNIQUE (userid, follower_id),"
                     "FOREIGN KEY (userid)"
                     "  REFERENCES profiles (userid)"
                     "    ON DELETE CASCADE,"
                     "FOREIGN KEY (follower_id)"
                     "  REFERENCES profiles (userid)"
                     "    ON DELETE CASCADE);")
