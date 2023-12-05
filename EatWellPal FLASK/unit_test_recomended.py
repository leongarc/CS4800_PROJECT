#Author: Uriel Alvarez


import unittest
from unittest.mock import Mock, patch, MagicMock
from connectors import recomendedMeal


class TestMealConnector(unittest.TestCase):
    # connect to recommended meal page
    def setUp(self):
        self.app = recomendedMeal.MealConnector(db_name='database.db')

    def tearDown(self):
        # Clean up resources, e.g., close the database connection
        pass

    # login to our test user account
    def login(self, db_name):
        test = self.app.login('test', 'test')

    def test_create_meal_dataframe(self):
        mock_cursor = Mock()
        mock_cursor.fetchall.return_value = [("Recipe1", "Ingredient1"), ("Recipe2", "Ingredient2")]
        mock_conn = Mock()
        mock_conn.cursor.return_value = mock_cursor

        with patch("sqlite3.connect", return_value=mock_conn):
            self.app.create_meal_dataframe()

        self.assertIsNotNone(self.app.meal_df)

    def test_initialize_tfidf(self):
        self.app.create_meal_dataframe = Mock()

        self.app.tfidf_vectorizer = Mock()
        self.app.tfidf_vectorizer.fit_transform.return_value = Mock()
        self.app.tfidf_matrix = Mock()

        self.app.initialize_tfidf()

        self.app.tfidf_vectorizer.fit_transform.assert_called_once_with(self.app.meal_df['Ingredients'])
        self.app.tfidf_matrix.assert_called_once_with(self.app.tfidf_vectorizer.fit_transform.return_value)



    def test_process_meal_data(self):
        # Set up test parameters
        self.app.create_meal_dataframe = Mock()
        self.app.initialize_tfidf = Mock()
        self.app.get_ingredients = Mock(return_value="Chicken Salad")
        self.app.get_ingredients_group = Mock(return_value="Veggies Mix")

        self.app.tfidf_vectorizer = Mock()
        self.app.tfidf_matrix = Mock()
        self.app.linear_kernel = Mock()
        self.app.get_recommendations = Mock(return_value=["Meal1", "Meal2"])

        result = self.app.process_meal_data()

        self.app.create_meal_dataframe.assert_called_once()
        self.app.initialize_tfidf.assert_called_once()
        self.app.get_ingredients.assert_called_once()
        self.app.get_ingredients_group.assert_called_once()

        self.app.tfidf_vectorizer.transform.assert_called_with(["Chicken Salad"])
        self.app.linear_kernel.assert_called_with(self.app.tfidf_vectorizer.transform.return_value, self.app.tfidf_matrix)
        self.app.get_recommendations.assert_called_with("Chicken Salad", self.app.linear_kernel.return_value)


    # Define a function to get meal recommendations based on user preferences
    def test_recommendations(self):
       # Set up test parameters
        user_input = "Chicken Salad"
        cosine_sim = Mock()

        self.app.tfidf_vectorizer = Mock()
        self.app.tfidf_matrix = Mock()

        result = self.app.get_recommendations(user_input, cosine_sim)

        self.app.tfidf_vectorizer.transform.assert_called_once_with([user_input])

        cosine_sim_user = self.app.tfidf_vectorizer.transform.return_value

        cosine_sim.assert_called_once_with(cosine_sim_user, self.app.tfidf_matrix)

        self.app.meal_df['Name'].iloc.__getitem__.assert_called_once_with(slice(None, 10, None))
        
        expected_result = self.app.meal_df['Name'].iloc.__getitem__.return_value
        self.assertEqual(result, expected_result)

       

    def test_new_meals(self):
        # Mock database connection and cursor
        mock_cursor = Mock()
        mock_conn = Mock()
        mock_conn.cursor.return_value = mock_cursor

        # Patch the sqlite3.connect method to return the mock connection
        with unittest.mock.patch("sqlite3.connect", return_value=mock_conn):
            # Call the method to be tested
            result = self.app.new_meals()

        # Assertions
        mock_cursor.execute.assert_called_once_with(
            "SELECT RecipeName, id FROM recipes ORDER BY ID DESC LIMIT 10"
        )
        expected_result = [(1, 'Recipe1'), (2, 'Recipe2')]  # Adjust based on your test case
        self.assertEqual(result, expected_result)

    

    def test_get_ingredients_group(self):
          # Mock database connection and cursor
        mock_cursor = Mock()
        mock_conn = Mock()
        mock_conn.cursor.return_value = mock_cursor

        # Patch the sqlite3.connect method to return the mock connection
        with unittest.mock.patch("sqlite3.connect", return_value=mock_conn):
            # Call the method to be tested
            result = self.app.get_ingredients_group()

        # Assertions
        mock_cursor.execute.assert_called_once_with(
            "SELECT FoodName FROM calorie_intake WHERE Timestamp >= DATE('now', '-30 days');"
        )
        self.assertEqual(result, '  '.join(mock_cursor.fetchall.return_value))

        
    def test_get_ingredients(self):
        # Set up test parameters
        self.app.user_id = 1  # Assuming a user ID is set in the instance

        # Mock database connection and cursor
        mock_cursor = Mock()
        mock_conn = Mock()
        mock_conn.cursor.return_value = mock_cursor

        # Patch the sqlite3.connect method to return the mock connection
        with unittest.mock.patch("sqlite3.connect", return_value=mock_conn):
            # Call the method to be tested
            result = self.app.get_ingredients()

        # Assertions
        mock_cursor.execute.assert_called_once_with(
            "SELECT FoodName FROM calorie_intake WHERE user_id = ? AND Timestamp >= DATE('now', '-10 days');",
            (self.app.user_id,),
        )
        self.assertEqual(result, '  '.join(mock_cursor.fetchall.return_value))

            
    def test_login(self):
        # Set up test parameters
        username = "test_user"
        password = "test_password"

        # Mock database connection and cursor
        mock_cursor = Mock()
        mock_conn = Mock()
        mock_conn.cursor.return_value = mock_cursor

        # Patch the sqlite3.connect method to return the mock connection
        with unittest.mock.patch("sqlite3.connect", return_value=mock_conn):
            # Call the method to be tested
            result = self.app.login(username, password)

        # Assertions
        mock_cursor.execute.assert_called_once_with(
            "SELECT user_id FROM users WHERE username = ? AND password = ?", (username, password)
        )
        self.assertEqual(result, mock_cursor.fetchone.return_value[0])


    def test_get_meal_data_by_column(self):
        # Set up test parameters
        recipe_id = "Spaghetti_ID"
        column_name = "Calories"

        # Mock database connection and cursor
        mock_cursor = Mock()
        mock_conn = Mock()
        mock_conn.cursor.return_value = mock_cursor

        # Patch the sqlite3.connect method to return the mock connection
        with unittest.mock.patch("sqlite3.connect", return_value=mock_conn):
            # Call the method to be tested
            result = self.app.get_meal_data_by_column(recipe_id, column_name)

        # Assertions
        mock_cursor.execute.assert_called_once_with(
            f"SELECT {column_name} FROM recipes WHERE RecipeName = ?", (recipe_id,)
        )
        self.assertEqual(result, mock_cursor.fetchone.return_value)


    def test_add_meal_intake(self):
        # Set up test parameters
        recipe_name = "Spaghetti"
        user_id = 1
        serving = 2
        recipe_calories = 500
        time = "2023-01-01 12:00:00"

        # Mock database connection and cursor
        mock_cursor = Mock()
        mock_conn = Mock()
        mock_conn.cursor.return_value = mock_cursor

        # Patch the sqlite3.connect method to return the mock connection
        with unittest.mock.patch("sqlite3.connect", return_value=mock_conn):
            # Call the method to be tested
            self.app.add_meal_intake(recipe_name, user_id, serving, recipe_calories, time)

        # Assertions
        mock_cursor.execute.assert_called_once_with(
            "SELECT MAX(ID) FROM calorie_intake"
        )
        mock_cursor.fetchone.assert_called_once()
        mock_cursor.execute.assert_called_with(
            "INSERT INTO calorie_intake (ID, FoodName, Quantity, TotalCalories, Timestamp, user_id) VALUES (?,?,?,?,?,?)",
            (mock_cursor.fetchone.return_value[0] + 1, recipe_name, serving, recipe_calories, time, user_id),
        )


    def test_search_meal(self):
        # Set up mock data for search query
        search_query = "Chicken"

        # Set up mock cursor and connection
        mock_cursor = Mock()
        mock_cursor.fetchall.return_value = [("Chicken Curry",), ("Grilled Chicken",)]
        mock_conn = Mock()
        mock_conn.cursor.return_value = mock_cursor

        # Patch the sqlite3.connect method to return the mock connection
        with unittest.mock.patch("sqlite3.connect", return_value=mock_conn):
            # Call the method to be tested
            results = self.app.search_meal(search_query)

        # Assertions
        mock_cursor.execute.assert_called_once_with("SELECT RecipeName FROM recipes WHERE RecipeName LIKE ?", ('%Chicken%',))
        self.assertEqual(results, [("Chicken Curry",), ("Grilled Chicken",)])
    
if __name__ == '__main__':
    unittest.main()

