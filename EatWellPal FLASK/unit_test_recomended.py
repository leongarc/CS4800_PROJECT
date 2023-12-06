#Author: Uriel Alvarez
#unit testing for recomendedMeal.MealConnector

import unittest
import sqlite3
import pandas as pd
from datetime import datetime, date
from connectors import recomendedMeal
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import os


class TestMealConnector(unittest.TestCase):
    # connect to recommended meal page
    def setUp(self):
        self.db_name = "test.db" 
        self.app = recomendedMeal.MealConnector(self.db_name)
        self.tearDown()
        self.create_test_data()

    def tearDown(self):
        # Erase all tables and data
        with sqlite3.connect(self.db_name) as conn:
            conn.execute("DROP TABLE IF EXISTS recipes")
            conn.execute("DROP TABLE IF EXISTS users")
            conn.execute("DROP TABLE IF EXISTS calorie_intake")
            conn.execute("DROP TABLE IF EXISTS Favorite_meals")
            conn.execute("DROP TABLE IF EXISTS  Calories")
        if os.path.exists(self.db_name):
            os.remove(self.db_name)
    def create_test_data(self):

        with sqlite3.connect(self.db_name) as conn:
            # Make Table
            conn.execute("CREATE TABLE recipes (RecipeName TEXT, Ingredients TEXT, ID INT)")
            conn.execute("CREATE TABLE users (email TEXT, password TEXT, user_id INT, username TEXT)")
            conn.execute("CREATE TABLE calorie_intake (ID INT, FoodName TEXT, Quantity INT, TotalCalories INT, Timestamp DATETIME, user_id INT)")
            conn.execute("CREATE TABLE Favorite_meals (User_id INT, FoodName TEXT, food_id INT)")
            conn.execute("CREATE TABLE Calories (calories REAL, name TEXT);")
            
     
            time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # insert test data
            conn.execute("INSERT INTO recipes (RecipeName, Ingredients, ID) VALUES (?, ?, ?), (?, ?, ?)", 
                         ("Meal1", "Rice, Beans, Chicken", '1', "Meal2", "Eggs, Ham, Bacon", '2'))
            conn.execute("INSERT INTO users (email , password, user_id, username) VALUES (?, ?, ?, ?), (?, ?, ?, ?)", 
                         ("test", "test", '1', "test", 'example', 'example', '2', "example"))
            conn.execute("INSERT INTO calorie_intake (ID, FoodName , Quantity , TotalCalories , Timestamp , user_id ) VALUES (?, ?, ?, ?, ?, ?), (?, ?, ?, ?, ?, ?)", 
                         ("1", "Meal1", "1", '400', time, "1", "2", "Meal2", "1", '300', time, "2"))
            conn.execute("INSERT INTO Favorite_meals (User_id, FoodName, food_id) VALUES (?, ?, ?), (?, ?, ?)", 
                         ("1", "Meal1", "1", "2", "Meal2", "2"))
            conn.execute("INSERT INTO CALORIES (calories, name) VALUES (100, 'Test Ingredient');")

    def test_create_meal_dataframe(self):
        self.app.create_meal_dataframe()

        # Check if the DataFrame is not empty and has the expected columns
        self.assertFalse(self.app.meal_df.empty)

        expected_columns = ['Name', 'Ingredients']
        self.assertListEqual(list(self.app.meal_df.columns), expected_columns)

        # Check if specific data is present in the DataFrame
        self.assertTrue(('Meal1', 'Rice, Beans, Chicken') in zip(self.app.meal_df['Name'], self.app.meal_df['Ingredients']))

    def test_initialize_tfidf(self):
        self.app.create_meal_dataframe()

        self.app.initialize_tfidf()

        # Check if the TF-IDF Vectorizer and Matrix are initialized
        self.assertIsNotNone(self.app.tfidf_vectorizer)
        self.assertIsNotNone(self.app.tfidf_matrix)

    def test_process_meal_data(self):
        self.app.create_meal_dataframe()
        self.app.initialize_tfidf()

        user_input, group_input, recommendations_user, recommendations_group, new_meals = self.app.process_meal_data('1')

        # Check the outputs based on your expectations
        self.assertIsInstance(user_input, str)
        self.assertIsInstance(group_input, str)
        self.assertIsInstance(recommendations_user, pd.Series)
        self.assertIsInstance(recommendations_group, pd.Series)
        self.assertIsInstance(new_meals, list)

    def test_recommendations(self):
       # Set up test parameters
        self.app.create_meal_dataframe()
        self.app.initialize_tfidf()

        # Call the method you want to test
        user_input = "Rice, Beans"
        user_tfidf = self.app.tfidf_vectorizer.transform([user_input])
        cosine_sim_user = linear_kernel(user_tfidf, self.app.tfidf_matrix)
        recommendations_user = self.app.get_recommendations(user_input, cosine_sim_user)

        # Check the output based on your expectations
        self.assertIsInstance(recommendations_user, pd.Series)

    def test_new_meals(self):
        self.app.create_meal_dataframe()
        new_meals = self.app.new_meals()

        #check for output
        self.assertIsInstance(new_meals, list)

    def test_get_ingredients_group(self):
        ingredients_group = self.app.get_ingredients_group()

        # make sure output is correct
        self.assertIsInstance(ingredients_group, str)

    def test_get_ingredients(self):
        ingredients = self.app.get_ingredients('1')

        # Check the output based on your expectations
        self.assertIsInstance(ingredients, str)

    def test_login(self):
        test = self.app.login('test', 'test')

        self.assertIsNotNone(test)
        self.assertEqual(test, 1)

    def test_get_meal_data_by_column(self):
        recipe_id = "Meal1"
        column_name = "Ingredients"
        meal_data = self.app.get_meal_data_by_column(recipe_id, column_name)

        # Check the output 
        self.assertIsInstance(meal_data, tuple)

    def test_add_meal_intake(self):
        # Set up test parameters
        recipe_name = "Meal2"
        user_id = 1
        serving = 1
        recipe_calories = 500
        time = "2023-01-01 12:00:00"
        self.app.add_meal_intake(recipe_name, user_id, serving, recipe_calories, time)

        with sqlite3.connect(self.db_name) as conn:
            result = conn.execute("SELECT * FROM calorie_intake WHERE FoodName = ? AND user_id = ?", (recipe_name, user_id)).fetchone()
            self.assertIsNotNone(result)

    def test_search_meal(self):
        search_query = "Meal"
        result = self.app.search_meal(search_query)

        # Check if the search result is as expected
        self.assertGreater(len(result), 0)
        self.assertIn("Meal1", result)
        self.assertIn("Meal2", result)


    def test_add_meal_favorites(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()

            # add test data to recipe
            self.app.add_meal_favorites("Meal1", user_id=1)

            # Verify 
            cursor.execute("SELECT COUNT(*) FROM Favorite_Meals WHERE User_id = 1 AND FoodName = 'Meal1';")
            result = cursor.fetchone()[0]
            self.assertEqual(result, 1)


    def test_dailyintake(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()

            # Add test data
            cursor.execute("INSERT INTO calorie_intake (FoodName, user_id, Timestamp) VALUES ('Meal1', 1, ?);", (datetime.now(),))


            result = self.app.dailyintake(user_id=1)

            # Verify
            self.assertIn('Meal1', result)


    def test_add_ingredient(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()

            self.app.add_ingredient(user_id='1', ingredient_name='Test Ingredient', quantity=150)

            # Verify
            cursor.execute("SELECT COUNT(*) FROM calorie_intake WHERE FoodName = 'Test Ingredient';")
            result = cursor.fetchone()[0]
            self.assertEqual(result, 1)


if __name__ == '__main__':
    unittest.main()
    

