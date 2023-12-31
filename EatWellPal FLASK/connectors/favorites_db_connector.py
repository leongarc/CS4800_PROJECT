# Favorites DB connector
# This controller grabs favorites data from the database.db
# and returns the called information depending on the user who called it.
# By Leo Garcia

import sqlite3
import json
#import os
#db_path = os.path.join(os.getcwd() + '/databases/users.db')

class FavoritesDBConnector:
    db_name = "database.db"
    def __init__(self, userid):
        self.user_id = userid
        self.conn = self.connect_to_db()
        self.cur = self.conn.cursor()
    
    # Function that trys to connect to database and catches to handle the error
    def connect_to_db(self):
        try:
            conn = sqlite3.connect(self.db_name)
            return conn
        except Exception:
            print("DB does not exist/Error opening")
            return False

    # Returns the user's favorites in a Python List
    # Returns None if no favorites data exists
    def get_favorites(self):
        self.cur.execute("SELECT FoodName,\
                          food_id\
                          FROM Favorite_Meals\
                          WHERE User_id = ?", (str(self.user_id),))
        result = self.cur.fetchall()
        
        if result:
            return result
        else:
            return None

    # Using this one
    # Alternate version of update_favorites() function
    def insert_favorites(self, food_name, food_id):
        exist = self.favorite_exists(food_id)
        # Returns True if entry exists
        if exist:
            return exist
        else:
            self.cur.execute("INSERT INTO Favorite_Meals\
                            (User_id,\
                            FoodName,\
                            food_id)\
                            VALUES (?,?,?)", (self.user_id, food_name, food_id))
            self.conn.commit()

    # Delete favorite meal from user's list
    def delete_favorites(self, food_id):
        self.cur.execute("DELETE FROM Favorite_Meals\
            WHERE User_id = ? AND food_id = ?", (str(self.user_id), food_id))
        
        self.conn.commit()
    
    # Checks to see if entry exists
    def favorite_exists(self, food_id):
        self.cur.execute("SELECT User_id\
                          FROM Favorite_Meals\
                          WHERE User_id = ? AND food_id = ?", (str(self.user_id), food_id))
        result = self.cur.fetchone()

        if result:
            return True
        else:
            return False

    def get_recipe(self, food_id):
        num = json.loads(food_id)
        self.cur.execute("SELECT RecipeName, Calories FROM recipes WHERE id = ?", (num,))
        result = self.cur.fetchall()

        if result:
            return result
        else:
            return False
    # Used to close the connectioin to the database when no longer needed
    def close_connection(self):
        self.conn.close()


    
    # Keeping it for reference
    # This is original update function, may or may not use
    # Was trying to find a way to successfully add the favorites list in a JSON format
    # While it adds the data succesfully, it adds it in a weird way
    # Works with the 'users.db' database not the current 'database.db'
    def update_favorties_do_not_use(self, data):
        current_favorites = self.get_favorites()
        print(current_favorites[0])
        if current_favorites is None:
            self.cur.execute("UPDATE userinfo\
                              SET favorites = ?\
                              WHERE user_id = ?", (json.dumps(data), str(self.user_id)))
        else:
            c_f = json.dumps(current_favorites[0])
            print(c_f)
            for position in data:
                self.cur.execute("UPDATE userinfo\
                                SET favorites = json_set(?,'$[#]',?)\
                                WHERE user_id = ?", (c_f, position, str(self.user_id)))
                # Printing used for testing
                print(position)
                
                c_f += str(position)
        self.conn.commit()