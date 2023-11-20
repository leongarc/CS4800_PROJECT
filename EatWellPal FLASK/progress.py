import sqlite3
from flask import Flask, render_template

app = Flask(__name__)

# Define your ProgressBar, WeightProgressChart, and UserInterface classes here

@app.route('/')
def index():
    return "Welcome to the Progress Page!"

@app.route('/calorie_progress/<int:user_id>')
def calorie_progress(user_id):
    # Create a UserInterface instance
    user_interface = UserInterface(user_id)

    # Get and display calorie data
    conn = sqlite3.connect("calorie_intake.db")
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
