# Faorites DB connector. This controller assits in grabing favorites data from the users.db
# and returns the called information depending on the user who called it.
# By Leo Garcia

import sqlite3
import os
db_path = os.path.join(os.getcwd() + '/databases/users.db')

class FavoritesDBConnector:

    def __init__(self, path=db_path):
        self.user_db = path
        self.conn = self.connect_to_db()
        self.cur = self.conn.cursor()
    
    def connect_to_db(self):
        try:
            conn = sqlite3.connect(self.user_db)
            return conn
        except OSError:
            print("DB does not exist/Error opening")

    def get_favorites(self, user_id):
        # need to create favorites column in users.db
        # need to set up favorites data in a JSON format since arrays aren't suppported in SQLite
        self.cur.execute("SELECT favorites FROM userinfo WHERE user_id = ?", (str(user_id)))
        result = self.cur.fetchone()
        if result: 
            return result
        else:
            result = None
            return result
    # Still need to work on update_favorites
    def update_favorites():
        pass

    def close_connection(self):
        self.conn.close()