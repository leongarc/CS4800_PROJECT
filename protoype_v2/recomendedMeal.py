#Author: Uriel Alvarez

import sqlite3
import pandas as pd
from datetime import datetime, date
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import os 
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class MealConnector:
    def __init__(self, food_db_name, intake_db_name, users_db_name):
        self.food_db_name = food_db_name
        self.intake_db_name = intake_db_name
        self.users_db_name = users_db_name
        self.user_id = None
        self.meal_df = None
        self.tfidf_vectorizer = None
        self.tfidf_matrix = None
        self.cosine_sim = None

    def create_meal_dataframe(self):
        # Connect to the SQLite database and fetch meal data
        conn = sqlite3.connect('meals.db')
        cursor = conn.cursor()
        cursor.execute('SELECT RecipeName, Ingredients FROM recipes')
        data = cursor.fetchall()
        conn.close()

        # Create a DataFrame from the meal data
        self.meal_df = pd.DataFrame(data, columns=['Name', 'Ingredients'])

    def initialize_tfidf(self):
        # Initialize the TF-IDF Vectorizer
        self.tfidf_vectorizer = TfidfVectorizer(stop_words='english')

        # Fit and transform the TF-IDF Vectorizer on the Ingredients column
        self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(self.meal_df['Ingredients'])

        # Calculate the cosine similarity matrix
        self.cosine_sim = linear_kernel(self.tfidf_matrix, self.tfidf_matrix)

    def process_meal_data(self):
        # Fetch and create the DataFrame
        self.create_meal_dataframe()

        # Initialize TF-IDF Vectorizer and calculate cosine similarity
        self.initialize_tfidf()

        # Take user input and provide meal recommendations
        user_input = self.get_ingredients()
        group_input = self.get_ingredients_group()

        user_tfidf = self.tfidf_vectorizer.transform([user_input])
        cosine_sim_user = linear_kernel(user_tfidf, self.tfidf_matrix)

        group_tfidf = self.tfidf_vectorizer.transform([group_input])
        cosine_sim_group = linear_kernel(group_tfidf, self.tfidf_matrix)

        recommendations_user = self.get_recommendations(user_input, cosine_sim_user)
        recommendations_group = self.get_recommendations(group_input, cosine_sim_group)
        new_meals = self.new_meals()

        print(user_input)
        print(group_input)
        print("\nRecommended Meals (Based on User Input):")
        print(recommendations_user)
        print("\nRecommended Meals (Based on Group Input):")
        print(recommendations_group)
        print("\nRecently Added Meals:")
        print(new_meals)

    # Define a function to get meal recommendations based on user preferences
    def get_recommendations(self, user_input, cosine_sim):
        user_tfidf = self.tfidf_vectorizer.transform([user_input])
        cosine_scores = linear_kernel(user_tfidf, self.tfidf_matrix)
        meal_scores = list(enumerate(cosine_scores[0]))
        meal_scores = sorted(meal_scores, key=lambda x: x[1], reverse=True)
        top_meal_indices = [score[0] for score in meal_scores]
        return self.meal_df['Name'].iloc[top_meal_indices]

    def new_meals(self):
        # Connect to the SQLite database and fetch meal data
        conn = sqlite3.connect('meals.db')
        cursor = conn.cursor()
        cursor.execute('SELECT RecipeName, Calories FROM recipes WHERE RecipeName <> "" ORDER BY ID DESC LIMIT 10')
        data = cursor.fetchall()
        conn.close()

        for recipe_name, calories in data:
            if recipe_name and calories:
                return ((recipe_name, calories))

    def get_ingredients_group(self):
        intake_conn = sqlite3.connect(self.intake_db_name)
        intake_cursor = intake_conn.cursor()

        intake_cursor.execute("SELECT FoodName FROM calorie_intake WHERE Timestamp >= DATE('now', '-30 days');" )
        results = intake_cursor.fetchall()
        intake_conn.close()

        if results:
            food_name = [result[0] for result in results]
            user_input = '  '.join(food_name).lower()
            print("grooup test",user_input)
            return user_input
        else:
            return ''
        
    def get_ingredients(self):
        intake_conn = sqlite3.connect(self.intake_db_name)
        intake_cursor = intake_conn.cursor()

        intake_cursor.execute("SELECT FoodName FROM calorie_intake WHERE user_id = ? and Timestamp >= DATE('now', '-10 days');",(self.user_id,) )
        results = intake_cursor.fetchall()
        intake_conn.close()

        if results:
            food_name = [result[0] for result in results]
            user_input = '  '.join(food_name).lower()
            print("user test",user_input)
            return user_input
        else:
            print("nnoot results")
            return ''
            
    def login(self, username, password):
        user_conn = sqlite3.connect(self.users_db_name)
        user_cursor = user_conn.cursor()
        user_cursor.execute("SELECT user_id FROM users WHERE username = ? AND password = ?", (username, password))
        result = user_cursor.fetchone()
        user_conn.close()
        if result:
            self.user_id = result[0]
        return self.user_id


# Prompt the user to enter their username and password
username = input("Enter your username: ")
password = input("Enter your password: ")

# Create an instance of MealConnector
tracker = MealConnector("ingredients.db", "calorie_intake.db", "users.db")

# Attempt to log in
user_id = tracker.login(username, password)

if user_id is not None:
    # Process meal data, initialize TF-IDF, and get recommendations
    tracker.process_meal_data()
else:
    print("Login failed. Please check your credentials.")