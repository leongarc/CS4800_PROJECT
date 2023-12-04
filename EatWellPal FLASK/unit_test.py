#Author: Luis Ochoa


import unittest
from connectors import user_db_connector as users

class TestAccountManagement(unittest.TestCase):

    #this is like the __init__ function for regular classes
    #connects to accountManagement class
    def setUp(self):
        # Create a temporary database for testing
        self.app = users.AccountManagement()

    #This happens at the end of each function test
    #Deletes the extra account created if needed
    def tearDown(self):
        try:
            test = self.app.login("test_user", "password")
            self.app.delete_account(test)
        except:
            pass
        self.app.close_connection()

    #Test the signup_check method  
    def test_signup_check(self):
        test = self.app.signup_check('test_username', 'test_email')
        
        #Checks to make sure this is not in the system already, which is shouldn't
        #the flip side is tested later as well in the create account test
        self.assertFalse(test)
     
    # Test the create_account method       
    def test_create_account(self):
        self.app.create_account("test_user", "test@example.com", "password", "John", "Doe", 70, 180, 75, "None", "Male")
        test = self.app.login('test_user', 'password')
        
        #Creates an account- and checks to make sure it is created
        #the flip side is tested later as well in the create account test
        self.assertIsNotNone(test)


    #Test the login function- specifically if the user is trying to login without
    #correct credential
    def test_login(self):
        test = self.app.login("non-existing_username", "password")
        assert bool(test) == False
        # Add more test cases as needed

    def test_get_info(self):
        # Test the get_info method
        user_object = self.app.get_info(1)
        self.assertIsNotNone(user_object)


    def test_about_user(self):
        # Test the about_user method
        user_info = self.app.about_user(2)
        self.assertIsNotNone(user_info)
        # Add assertions to check if the returned user_info is correct
        # Add more test cases as needed

    def test_update_info(self):
        # Test the update_info method
        self.app.create_account("test_user", "test@example.com", "password", "John", "Doe", 70, 180, 75, "None", "Male")
        test = self.app.login('test_user', 'password')

        self.app.update_info(test, "Updated", "User", 75, 175, 80, "None", "Female")
        test = self.app.login('test_user', 'password')
        self.assertIsNotNone(test)
        
        # Add assertions to check if the user information is updated correctly
        # Add more test cases as needed
        
