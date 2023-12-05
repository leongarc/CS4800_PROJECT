import sqlite3
from flask import Flask, render_template

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

@app.route('/')
def index():
    return "Welcome to the Progress Page!"

@app.route('/calorie_progress/<int:user_id>')
def calorie_progress(user_id):
    # Create a UserInterface instance
    user_interface = UserInterface(user_id)

    # Get and display calorie data
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT consumed_calories, daily_calorie_goal FROM calorie_data WHERE user_id=?", (user_id,))
    data = cursor.fetchone()

    if data:
        consumed_calories, daily_calorie_goal = data
        calorie_progress = {
            "consumed_calories": consumed_calories,
            "daily_calorie_goal": daily_calorie_goal
        }
    else:
        calorie_progress = None

    conn.close()

    return render_template('calorie_progress.html', user_interface=user_interface, calorie_progress=calorie_progress)

@app.route('/weight_progress/<int:user_id>')
def weight_progress(user_id):
    # Create a WeightProgressChart instance
    weight_chart = WeightProgressChart(user_id)

    return render_template('weight_progress.html', weight_chart=weight_chart)

if __name__ == '__main__':
    app.run(debug=True)
