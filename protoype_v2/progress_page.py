#This page will hold the command line UI for the progress page
#this page will need a progress bar that shows how much calories they have consumed and how much they need left
#this page will need a chart that shows their weight progress

#Author: Jack W.
## separate into objects and classes instead of functions ##

import sqlite3
import matplotlib.pyplot as plt
import numpy as np

# Function to display a text-based progress bar
def print_progress_bar(current, total, length=50):
    progress = int(length * current / total)
    bar = "[" + "=" * progress + " " * (length - progress) + "]"
    percent = f"{(current / total) * 100:.2f}%"
    print(f"{bar} {percent} - {current}/{total}")

# Function to plot weight progress chart
def plot_weight_progress(user_id):
    conn = sqlite3.connect("weight_progress.db")
    cursor = conn.cursor()

    cursor.execute("SELECT date, weight FROM weight_data WHERE user_id=?", (user_id,))
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

def main(user_id):
    # Connect to the database and retrieve calorie consumption data
    conn = sqlite3.connect("calorie_intake.db")
    cursor = conn.cursor()

    cursor.execute("SELECT consumed_calories, daily_calorie_goal FROM calorie_data WHERE user_id=?", (user_id,))
    data = cursor.fetchone()

    if data:
        consumed_calories, daily_calorie_goal = data
        print(f"Consumed Calories: {consumed_calories} / Daily Goal: {daily_calorie_goal}")
        print("Calorie Consumption Progress:")
        print_progress_bar(consumed_calories, daily_calorie_goal)
    else:
        print("No calorie consumption data available.")

    # Plot weight progress chart
    plot_weight_progress(user_id)

if __name__ == "__main__":
    user_id = input("Enter your user ID: ")

    try:
        user_id = int(user_id)
    except ValueError:
        print("Invalid user ID. Please enter a valid user ID.")
    else:
        main(user_id)


#A function that ask the user if they want to switch tabs ie Progress, Account, Favorite or sign out/quit application
#Have their response return  to the main page
#6. Home, 7. Progress, 8. Favorite, 9. Account, 0. Quit
