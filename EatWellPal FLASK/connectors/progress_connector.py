import sqlite3
import sqlite3
from datetime import date

#Author Jack W.
class ProgressDBConnector():
    def __init__(self):
        self.db_name = 'database.db'


    def get_calorie_data(self, user_id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        today = date.today()
        today_date = today.strftime("%Y/%m/%d")
        today_date = today_date.replace("/", "-")



        cursor.execute("SELECT TotalCalories FROM calorie_intake WHERE user_id=? and Timestamp >=?", (str(user_id),today_date))
        todays_intake = cursor.fetchall()

        print(todays_intake)
        #summing up totalcalories
        x = 0
        for meal in todays_intake:
            x += meal[0]

        cursor.execute("SELECT calorie_intake FROM userinfo WHERE user_id=?", (str(user_id)))
        user_intake = cursor.fetchone()
        user_intake = user_intake[0]
        conn.close()
        return x, user_intake if x != 0 else (0, user_intake)

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
