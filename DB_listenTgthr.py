import sqlite3
import datetime
from datetime import date


class DB:

    def __init__(self, db_name):
        """
        :param db_name: name of database
        """
        self.db_name = db_name  # name oif table
        self.conn = None        # connection to sqllite3
        self.cur = None         # cursor of table
        self._init_database()   # initiate db

    def _init_database(self):
        """
        :return: create the following databases:
        # 1) Users_tbl - user's main information. (Username, Mac_addr, Password)
        # 2) Songs_tbl - song's main information. (Song_name, Artist)
        # 3) Likes_tbl - song's like information. (Song_name, Username)
        # 4) Share_tbl - table with all shares dates (Song_name, Mac_addr, last_modified)

        """
        self.conn = sqlite3.connect(self.db_name + ".db")
        self.cur = self.conn.cursor()

        needed_tbls = {"users_tbl": "username VARCHAR(30), mac_addr VARCHAR(30), password CHAR(30)",
                       "songs_tbl": "song_name VARCHAR(30), artist VARCHAR(30)",
                       "likes_tbl": "song_name VARCHAR(30), username VARCHAR(30)",
                       "share_tbl": "song_name VARCHAR(30), mac_addr VARCHAR(30), last_modified CHAR(30)"}

        # create each table:
        for tbl in needed_tbls:
            sql_table = f"CREATE TABLE IF NOT EXISTS {tbl} ({needed_tbls[tbl]})"
            self.cur.execute(sql_table)

    # ------------
    # ------------

    def _check_exists(self, username):
        """
        :return: check if user exists in the system
        """
        user_exists = f"SELECT username FROM users_tbl WHERE username = '{username}'"
        self.cur.execute(user_exists)

        # does username exist?
        if len(self.cur.fetchall()) == 0:
            return False
        else:
            return True

    # ------------
    # ------------

    def _song_exist(self, song, artist):
        """
        :return: is the song in the share_tbl?
        """
        song_exists = f"SELECT song_name FROM songs_tbl WHERE song_name = '{song}' AND artist = '{artist}'"
        self.cur.execute(song_exists)

        # does song exist?
        if len(self.cur.fetchall()) == 0:
            return False
        else:
            return True

    # ------------
    # ------------

    def _check_like_exist(self, song_name, username):
        """
        :return: check if the client liked the song or not
        """
        like_exists = f"SELECT username FROM likes_tbl WHERE song_name = '{song_name}' AND username = '{username}' "
        self.cur.execute(like_exists)

        # does like exist?
        if len(self.cur.fetchall()) == 0:
            return False
        else:
            return True

    # ------------
    # ------------

    # enter new client into the system:
    def enter_client(self, username, mac_addr, password):
        """
        :return: Store new client's data in the database
        """
        # todo: create username exists for checkup
        if self._check_exists(username):
            print("sorry, username already taken!")
        else:
            sql_table = f"INSERT INTO users_tbl VALUES('{username}', '{mac_addr}', '{password}')"
            self.cur.execute(sql_table)
            self.conn.commit()

    # ------------
    # ------------

    def remove_client(self, username):
        """
        :return: remove the client from db
        """
        # check if user exist:
        # delete user from all tables:

        if self._check_exists(username):
            del_user = f"DELETE from users_tbl WHERE username = '{username}'"
            self.cur.execute(del_user)
            self.conn.commit()

    # ------------
    # ------------

    def add_song(self, song_name, artist, mac_addr):
        """
        :return: add the song to -
        # 1) add If doesn’t exist in song_tbl
        # 2) add \ modify date in share_data table
        """

        # add to song tbl if it doesnt exist there
        if not self._song_exist(song_name, artist):
            insert_song = f"INSERT INTO songs_tbl VALUES('{song_name}', '{artist}')"
            self.cur.execute(insert_song)
            self.conn.commit()

        exists_in_tbl = f"SELECT song_name FROM share_tbl WHERE song_name = '{song_name}' AND mac_addr = '{mac_addr}'"
        self.cur.execute(exists_in_tbl)

        # get current date date of modifying
        current_date = date.today()

        # if song exists - just want to mod date
        if len(self.cur.fetchall()) != 0:
            insert_song = f"Update share_tbl set last_modified = '{str(current_date)}' where" \
                f" song_name = '{song_name}' AND mac_addr = '{mac_addr}'"
            self.cur.execute(insert_song)
            self.conn.commit()

        # if song doesnt exist - add to table
        else:
            insert_song = f"INSERT INTO share_tbl VALUES('{song_name}', '{mac_addr}', '{str(current_date)}')"
            self.cur.execute(insert_song)
            self.conn.commit()

    # ------------
    # ------------

    def check_last_modified(self):
        """
        :return: delete everything modified earlier then a month ago
        """
        songs_shares = f"SELECT * FROM share_tbl"
        self.cur.execute(songs_shares)
        all_rows = self.cur.fetchall()

        dates_to_del = []

        if len(all_rows) != 0:
            for row in all_rows:
                # check row
                # 3 => (Song_name, Mac_addr, last_modified)
                mod_year = int(row[2].split("-")[0])
                mod_month = int(row[2].split("-")[1])
                mod_day = int(row[2].split("-")[2])

                # date of modification:
                mod_date = datetime.datetime(mod_year, mod_month, mod_day).date()
                # add to see if its been a month:
                end_date = mod_date + datetime.timedelta(days=30)

                if end_date <= datetime.date.today():
                    dates_to_del.append(mod_date)  # append date for future delete

        for date in dates_to_del:
            del_old_mods = f"DELETE from share_tbl where last_modified = '{date}'"
            self.cur.execute(del_old_mods)
            self.conn.commit()

    # ------------
    # ------------

    def verify_login(self, username, hushed_password):
        """
        :return: if user can be logged into the system - return true
        """
        flag = False
        # check fisrt username then password
        if self._check_exists(username):

            right_password = f"SELECT username FROM users_tbl WHERE username = '{username}' AND password = '{hushed_password}' "
            self.cur.execute(right_password)

            # does like exist?
            if len(self.cur.fetchall()) == 1:
                flag = True

        return flag

    # ------------
    # ------------

    def add_like(self, song_name, username):
        """
        :return: add like to the song
        """
        # is there a like already?
        like_exists = f"SELECT song_name FROM likes_tbl WHERE username = '{username}' AND song_name = '{song_name}' "
        self.cur.execute(like_exists)

        # if like doesnt exist
        if len(self.cur.fetchall()) == 0:
            like_exists = f"INSERT INTO likes_tbl VALUES('{song_name}', '{username}')"
            self.cur.execute(like_exists)
            self.conn.commit()

    # ------------
    # ------------

    def remove_like(self, song_name, username):
        """
        :return: delete like to given song
        """
        # is there a like already?
        like_exists = f"SELECT song_name FROM likes_tbl WHERE username = '{username}' AND song_name = '{song_name}' "
        self.cur.execute(like_exists)

        # if like exists
        if len(self.cur.fetchall()) == 1:
            del_like = f"DELETE from likes_tbl WHERE username = '{username}' AND song_name = '{song_name}'"
            self.cur.execute(del_like)
            self.conn.commit()

    # ----------


def main():
    db = DB("data_try")

    # ------- user data checks -------

    # enter a new user
    db.enter_client("reut", "reuts mac", "password")

    # check if user exists
    print("DOES USER CALLED REUT EXIST?", db._check_exists("reut"))
    print("DOES USER CALLED moshik EXIST?", db._check_exists("moshik"))

    # try entering the same user again:
    db.enter_client("reut", "reuts mac", "password")
    print("verified login of reut?", db.verify_login("reut", "password"))

    # ------- song data checks ---------

    # add song :
    db.add_song("shades_of", "lana", "reuts mac")
    # check if song exist
    print(db._song_exist("shades_of", "lana"))
    # add like
    db.add_like("reut", "shades_of")
    print(db._check_like_exist("reut", "shades_of"))
    db.remove_like("reut", "shades_of")
    print(db._check_like_exist("reut", "shades_of"))

    # ------ modifying check ------
    db.check_last_modified()


if __name__ == '__main__':
    main()
