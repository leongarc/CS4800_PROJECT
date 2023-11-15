import sqlite3
from datetime import datetime, date
import os 
os.chdir(os.path.dirname(os.path.abspath(__file__)))


class CalorieTracker:
    def __init__(self, food_db_name, intake_db_name, users_db_name):
        self.food_db_name = food_db_name
        self.intake_db_name = intake_db_name
        self.users_db_name = users_db_name
        self.user_id = user_id

    def add_ingredient(self, ingredient_name, quantity):
        food_conn = sqlite3.connect(self.food_db_name)
        food_cursor = food_conn.cursor()
        intake_conn = sqlite3.connect(self.intake_db_name)
        intake_cursor = intake_conn.cursor()

        # Retrieve calorie information from the food database
        food_cursor.execute("SELECT calories, name FROM CALORIES WHERE lower(name) LIKE ? ", ('%' + ingredient_name.lower() + '%',))
        result = food_cursor.fetchone()

        if result:
            calorie_per_100g = float(result[0])
            food_name = result[1]
            calorie = (calorie_per_100g / 100) * quantity

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Add the ingredient to the intake database
            intake_cursor.execute("INSERT INTO calorie_intake (FoodName, Quantity, TotalCalories, Timestamp, user_id) VALUES (?, ?, ?, ?, ?)",
                                  (food_name, quantity, calorie, timestamp, user_id))
            intake_conn.commit()

            print(f"Added {quantity}g of {food_name} ({calorie} calories) to your daily intake.")
        else:
            print(f"{ingredient_name} is not in the database. You can add custom ingredients.")

        food_conn.close()
        intake_conn.close()

    
#Author of add_meal Jack W.
class CalorieManager:
    def __init__(self, user_id, intake_db_name, users_db_name):
        self.user_id = user_id
        self.intake_db_name = intake_db_name
        self.users_db_name = users_db_name

    def add_meal(self, meal_name, calories):
        intake_conn = sqlite3.connect(self.intake_db_name)
        intake_cursor = intake_conn.cursor()

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Add the meal to the intake database
        intake_cursor.execute("INSERT INTO calorie_intake (FoodName, Quantity, TotalCalories, Timestamp, user_id) VALUES (?, ?, ?, ?, ?)",
                              (meal_name, 1, calories, timestamp, self.user_id))
        intake_conn.commit()

        print(f"Added {meal_name} to your daily intake with {calories} calories.")

        intake_conn.close()

    def get_daily_calories(self):
        intake_conn = sqlite3.connect(self.intake_db_name)
        intake_cursor = intake_conn.cursor()

        current_date = date.today().strftime("%Y-%m-%d")

        intake_cursor.execute("SELECT SUM(TotalCalories) FROM calorie_intake WHERE user_id = ? and DATE(Timestamp) = ?",(self.user_id, current_date,))
        result = intake_cursor.fetchone()
        intake_conn.close()

        if result:
            return result[0]
        else:
            return 0
        
    def get_calories_goal(self):
        intake_conn = sqlite3.connect(self.users_db_name)
        intake_cursor = intake_conn.cursor()

        intake_cursor.execute("SELECT calorie_intake FROM userinfo WHERE user_id = ?",(self.user_id,))
        result = intake_cursor.fetchone()
        intake_conn.close()

        if result:
            return result[0]
        else:
            return 0


# Create a login function to authenticate users
def login(username, password):
    user_conn = sqlite3.connect("users.db")
    user_cursor = user_conn.cursor()
    user_cursor.execute("SELECT user_id FROM users WHERE username = ? AND password = ?", (username, password))
    result = user_cursor.fetchone()
    user_conn.close()
    return result[0] if result else None

# Prompt the user to enter their username and password
username = input("Enter your username: ")
password = input("Enter your password: ")

# Attempt to log in
user_id = login(username, password)

if user_id is not None:
    # Successful login, create a CalorieTracker instance for the user
    tracker = CalorieTracker("ingredients.db", "calorie_intake.db", "users.db")
    
    while True:
        print("Options:")
        print("1. Add ingredient")
        print("2. Get daily calorie intake")
        print("3. Exit")
        choice = input("Select an option: ")

        if choice == '1':
            ingredient_name = input("Enter the ingredient name: ").lower()
            quantity = float(input("Enter the quantity (in grams): "))
            tracker.add_ingredient(ingredient_name, quantity)
        elif choice == '2':
            print(f"{username} daily calorie intake: {tracker.get_daily_calories()} calories out of {tracker.get_calories_goal()}")
        elif choice == '3':
            break

else:
    print("Invalid username or password. Please try again.")
