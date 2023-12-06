import unittest
from flask import Flask, current_user, render_template
from flask_testing import TestCase
import progress_connector
import plotly.express as px  

class TestProgressRoute(TestCase):

    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    def test_progress_route(self):
        # Mock the current_user object (assuming you are using Flask-Login)
        current_user.id = 1  # Set the user ID to a known value

        # Create a mock instance of the ProgressDBConnector
        class MockProgressDBConnector:
            def get_calorie_data(self, user_id):
                return (100, 2000)  # Mocked calorie data

        # Replace the real ProgressDBConnector with the mock
        your_app.progress_connector.ProgressDBConnector = MockProgressDBConnector

        # Create a mock instance of the MealConnector
        class MockMealConnector:
            def dailyintake(self, user_id):
                return {}  # Mocked intake data

        # Replace the real MealConnector with the mock
        your_app.recomendedMeal.MealConnector = MockMealConnector

        # Test the /progress route
        response = self.client.get('/progress')

        self.assertEqual(response.status_code, 200)
        self.assert_template_used('progress.html')

if __name__ == '__main__':
    unittest.main()
