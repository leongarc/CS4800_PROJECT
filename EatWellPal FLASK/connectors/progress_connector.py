import sqlite3
from flask import Flask, render_template
import sqlite3
import json
import os
db_path = os.path.join(os.getcwd() + '/databases/users.db')

#Author Jack W.

app = Flask(__name__)

# Class ProgressBar, Weight ProgressChart and UserInt

class ProgressBar:
    def __init__(self, current, total, length=50):
        self.current = current
        self.total = total
        self.length = length

    def display(self):
        progress = int(self.length * self.current / self.total)
        bar = "[" + "=" * progress + " " * (self.length - progress) + "]"
        percent = f"{(self.current / self.total) * 100:.2f}%"
        print(f"{bar} {percent} - {self.current}/{self.total}")

class WeightProgressChart:
    def __init__(self, user_id):
        self.user_id = user_id

    def plot(self):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("SELECT date, weight FROM weight_data WHERE user_id=?", (self.user_id,))
        data = cursor.fetchall()

        dates = [entry[0] for entry in data]
        weights = [entry[1] for entry in data]

        plt.plot(dates, weights, marker='o', linestyle='-', color='b')
        plt.xlabel("Date")
        plt.ylabel("Weight")
        plt.title("Weight Progress Chart")
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
        plt.show()

class UserInterface:
    def __init__(self, user_id):
        self.user_id = user_id

    def display_calorie_progress(self):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("SELECT consumed_calories, daily_calorie_goal FROM calorie_data WHERE user_id=?", (self.user_id,))
        data = cursor.fetchone()

        if data:
            consumed_calories, daily_calorie_goal = data
            print(f"Consumed Calories: {consumed_calories} / Daily Goal: {daily_calorie_goal}")
            print("Calorie Consumption Progress:")
            progress_bar = ProgressBar(consumed_calories, daily_calorie_goal)
            progress_bar.display()
        else:
            print("No calorie consumption data available")
