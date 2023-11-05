# This page will act like the middle man that connects the home_page UI to the database to get feature meals
# Author: Leo Garcia
import sqlite3
import User as u

class HomePageConnector():

    def __init__(self, user_id):
        self.user_id = user_id

    # Sends user's name to home page
    def get_user_name(self):
        user = u.User()
        user_info = user.get_user_by_id(self.user_id)
        # Used for extracting the necessay data from user info
        temp = []
        temp.append(user_info[2])
        temp.append(user_info[3])
        # Return only first and last name
        return temp
    
    # Sends user recommended meals to homepage
    def get_user_rec_meals(self):
        user = u.User()
        user_info = user.get_user_by_id(self.user_id)
        # Used for extracting the necessay data from user info
        temp = []
        temp.append(user_info[9])
        # Return rec meals
        return temp

