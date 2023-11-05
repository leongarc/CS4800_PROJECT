# Possible User class that is in charge of retrieving and manipulating user data
# Author: Leo Garcia
import sqlite3

class User:
    # initialize variables
    def __init__(self):
        DB_NAME = "users.db"
        self.conn = sqlite3.connect(DB_NAME)
        self.cursor = self.conn.cursor()
    # Insert new user. Still needs other columns
    def insert_user(self, first_name, last_name, body_weight):
        self.cursor.execute("INSERT INTO userinfo VALUES (NULL, ?, ?, ?)", (first_name, last_name, body_weight))
        self.conn.commit()
    # Gets a users information by id
    def get_user_by_id(self, id):
        self.cursor.execute("SELECT * FROM userinfo WHERE user_id = ?", (id,))
        return self.cursor.fetchone()
    # Update exiting user information
    def update_user(self, id, first_name, last_name, body_weight):
        self.cursor.execute("UPDATE userinfo SET first_name = ?, last_name = ?, body_weight = ? WHERE id = ?", (first_name, last_name, body_weight, id))
        self.conn.commit()

    def delete_user(self, id):
        self.cursor.execute("DELETE FROM userinfo WHERE id=?", (id,))
        self.conn.commit()

    def close_connection(self):
        self.conn.close()