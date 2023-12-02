# Faorites DB connector. This controller assits in grabing favorites data from the users.db
# and returns the called information depending on the user who called it.
# By Leo Garcia

import sqlite3
import os
import json
db_path = os.path.join(os.getcwd() + '/databases/users.db')
print(db_path)

class FavoritesDBConnector:

    def __init__(self, userid, path=db_path):
        self.user_id = userid
        self.path = path
        self.conn = self.connect_to_db()
        self.cur = self.conn.cursor()
    
    def connect_to_db(self):
        try:
            conn = sqlite3.connect(self.path)
            return conn
        except sqlite3.OperationalError:
            print("DB does not exist/Error opening")

    def get_favorites(self):
        # need to create favorites column in users.db
        # need to set up favorites data in a JSON format since arrays aren't suppported in SQLite
        self.cur.execute("SELECT favorites FROM userinfo WHERE user_id = ?", (str(self.user_id)))
        result = self.cur.fetchone()
        if result[0] is not None: 
            return result
        else:
            return None
    # Still need to work on update_favorites
    def update_favorties(self, data):
        current_favorites = self.get_favorites()
        print(current_favorites[0])
        if current_favorites is None:
            self.cur.execute("UPDATE userinfo\
                              SET favorites = ?\
                              WHERE user_id = ?", (json.dumps(data), str(self.user_id)))
        else:
            element = 0
            c_f = json.dumps(current_favorites[0])
            print(c_f)
            for position in data:
                self.cur.execute("UPDATE userinfo\
                                SET favorites = json_set(?,'$[#]',?)\
                                WHERE user_id = ?", (c_f, position, str(self.user_id)))
                print(position)
                
                c_f += str(position)
                element += 1
        self.conn.commit()

    def close_connection(self):
        self.conn.close()