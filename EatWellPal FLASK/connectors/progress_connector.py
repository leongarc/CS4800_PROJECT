import sqlite3
from flask import Flask, render_template
import sqlite3
import json
import os
db_path = os.path.join(os.getcwd() + '/databases/users.db')

#Author Jack W.
class ProgressDBConnector:
    def __init__(self, db_name):
        self.db_name = database.db

    def get_calorie_data(self, user_id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("SELECT consumed_calories, daily_calorie_goal FROM calorie_data WHERE user_id=?", (user_id,))
        data = cursor.fetchone()
        conn.close()

        return data if data else (0, 0)

    def get_weight_data(self, user_id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("SELECT date, weight FROM weight_data WHERE user_id=?", (user_id,))
        data = cursor.fetchall()
        conn.close()

        return data if data else []

    def update_calorie_data(self, user_id, consumed_calories, daily_calorie_goal):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("UPDATE calorie_data SET consumed_calories=?, daily_calorie_goal=? WHERE user_id=?", (consumed_calories, daily_calorie_goal, user_id))
        conn.commit()
        conn.close()

    def insert_weight_data(self, user_id, date, weight):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("INSERT INTO weight_data (user_id, date, weight) VALUES (?, ?, ?)", (user_id, date, weight))
        conn.commit()
        conn.close()
