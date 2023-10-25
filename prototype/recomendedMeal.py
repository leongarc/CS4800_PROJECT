import sqlite3
import pandas as pd
from datetime import datetime, date
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# Connect to the SQLite database and fetch meal data
conn = sqlite3.connect('newemeals.db')
cursor = conn.cursor()
cursor.execute('SELECT Recipe Name, Ingredients FROM meals')
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

class RecommendMeal:
    def __init__(self, food_db_name, intake_db_name, users_db_name):
        self.food_db_name = food_db_name
        self.intake_db_name = intake_db_name
        self.users_db_name = users_db_name
        self.user_id = user_id


    # Define a function to get meal recommendations based on user preferences
    def get_recommendations(user_input, cosine_sim=cosine_sim):
        user_tfidf = tfidf_vectorizer.transform([user_input])
        cosine_scores = linear_kernel(user_tfidf, tfidf_matrix)
        meal_scores = list(enumerate(cosine_scores[0]))
        meal_scores = sorted(meal_scores, key=lambda x: x[1], reverse=True)
        top_meal_indices = [score[0] for score in meal_scores]
        return meal_df['id'].iloc[top_meal_indices]

    def get_ingredients(self):
        intake_conn = sqlite3.connect(self.intake_db_name)
        intake_cursor = intake_conn.cursor()

        intake_cursor.execute("SELECT FoodName FROM calorie_intake WHERE user_id = ? and Timestamp >= DATE_SUB(CURDATE(), INTERVAL 10 DAY);",(self.user_id) )
        result = intake_cursor.fetchall()
        intake_conn.close()
        if result:
            return result[0]
        else:
            return 0


tracker = RecommendMeal("ingredients.db", "calorie_intake.db", "users.db")

# Take user input and provide meal recommendations
user_input = tracker.get_ingredients()
recommendations = tracker.get_recommendations(user_input)
print(user_input)
print("\nRecommended Meals:")
print(recommendations)
