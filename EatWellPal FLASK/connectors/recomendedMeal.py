#Author: Uriel Alvarez

import sqlite3
import pandas as pd
from datetime import datetime, date
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

class MealConnector:
    def __init__(self, db_name):
        self.db_name = db_name
        self.user_id = None
        self.meal_df = None
        self.tfidf_vectorizer = None
        self.tfidf_matrix = None
        self.cosine_sim = None

    def create_meal_dataframe(self):
        # Connect to the SQLite database and fetch meal data
        conn = sqlite3.connect(self.db_name)
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

        return user_input, group_input, recommendations_user, recommendations_group,new_meals

    # Define a function to get meal recommendations based on user preferences
    def get_recommendations(self, user_input, cosine_sim):
        user_tfidf = self.tfidf_vectorizer.transform([user_input])
        cosine_scores = linear_kernel(user_tfidf, self.tfidf_matrix)
        meal_scores = list(enumerate(cosine_scores[0]))
        meal_scores = sorted(meal_scores, key=lambda x: x[1], reverse=True)
        top_meal_indices = [score[0] for score in meal_scores][:10]
        return self.meal_df['Name'].iloc[top_meal_indices]

    def new_meals(self):
        # Connect to the SQLite database and fetch meal data
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT RecipeName, id FROM recipes ORDER BY ID DESC LIMIT 10')
        data = cursor.fetchall()
        conn.close()

        new_meal = []

        if data:
            new_meal = [(id, recipe_name) for recipe_name, id in data if recipe_name and id]
            return pd.DataFrame(new_meal)
        else:
            return pd.DataFrame()
    

    def get_ingredients_group(self):
        intake_conn = sqlite3.connect(self.db_name)
        intake_cursor = intake_conn.cursor()

        intake_cursor.execute("SELECT FoodName FROM calorie_intake WHERE Timestamp >= DATE('now', '-30 days');" )
        results = intake_cursor.fetchall()
        intake_conn.close()

        if results:
            food_name = [result[0] for result in results]
            user_input = '  '.join(food_name).lower()
            return user_input
        else:
            return ''
        
    def get_ingredients(self):
        intake_conn = sqlite3.connect(self.db_name)
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
            
    def login(self, username, password):
        user_conn = sqlite3.connect(self.db_name)
        user_cursor = user_conn.cursor()
        user_cursor.execute("SELECT user_id FROM users WHERE username = ? AND password = ?", (username, password))
        result = user_cursor.fetchone()
        user_conn.close()
        if result:
            self.user_id = result[0]
        return self.user_id

    def get_meal_data_by_column(self, recipe_id, column_name):
        meal_conn = sqlite3.connect(self.db_name)
        meal_cursor = meal_conn.cursor()
    
        query = f"SELECT {column_name} FROM recipes WHERE RecipeName = ?"
        meal_cursor.execute(query, (recipe_id,))
    
        result = meal_cursor.fetchone()
        if result:
            meal_conn.close()
        
        return result

    def add_meal_intake(self, recipe_id):
        user_conn = sqlite3.connect(self.db_name)
        user_cursor = user_conn.cursor()
        user_cursor.execute("INSERT INTO ", (recipe_id))
        result = user_cursor.fetchone()
        user_conn.close()
        if result:
            self.user_id = result[0]
        return self.user_id