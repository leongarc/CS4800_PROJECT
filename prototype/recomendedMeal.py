#Author: Uriel Alvarez

import sqlite3
import pandas as pd
from datetime import datetime, date
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import os 
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class RecommendMeal:
    def __init__(self, food_db_name, intake_db_name, users_db_name):
        self.food_db_name = food_db_name
        self.intake_db_name = intake_db_name
        self.users_db_name = users_db_name
        self.user_id = user_id


    # Define a function to get meal recommendations based on user preferences
    def get_recommendations(self, user_input, cosine_sim):
        user_tfidf = tfidf_vectorizer.transform([user_input])
        cosine_scores = linear_kernel(user_tfidf, tfidf_matrix)
        meal_scores = list(enumerate(cosine_scores[0]))
        meal_scores = sorted(meal_scores, key=lambda x: x[1], reverse=True)
        top_meal_indices = [score[0] for score in meal_scores]
        return meal_df['Name'].iloc[top_meal_indices]

    def get_ingredients(self):
        intake_conn = sqlite3.connect(self.intake_db_name)
        intake_cursor = intake_conn.cursor()

        intake_cursor.execute("SELECT FoodName FROM calorie_intake WHERE user_id = ? and Timestamp >= DATE('now', '-10 days');",(self.user_id,) )
        results = intake_cursor.fetchall()
        intake_conn.close()

        if results:
            food_name = [result[0] for result in results]
            user_input = '  '.join(food_name).lower()
            return user_input
        else:
            return ''
            
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
user_id = RecommendMeal.login(username, password)

tracker = RecommendMeal("ingredients.db", "calorie_intake.db", "users.db")

# Connect to the SQLite database and fetch meal data
conn = sqlite3.connect('meals.db')
cursor = conn.cursor()
cursor.execute('SELECT RecipeName, Ingredients FROM recipes')
data = cursor.fetchall()
conn.close()

# Create a DataFrame from the meal data
meal_df = pd.DataFrame(data, columns=['Name', 'Ingredients'])

# Initialize the TF-IDF Vectorizer
tfidf_vectorizer = TfidfVectorizer(stop_words='english')

# Fit and transform the TF-IDF Vectorizer on the Ingredients column
tfidf_matrix = tfidf_vectorizer.fit_transform(meal_df['Ingredients'])

# Calculate the cosine similarity matrix
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

# Take user input and provide meal recommendations
user_input = tracker.get_ingredients()
recommendations = tracker.get_recommendations(user_input, cosine_sim)
print(user_input)
print("\nRecommended Meals:")
print(recommendations)
