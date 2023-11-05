#This page will hold the command line UI for the home page
#This page will need to show the Username or First and Last name
#This page will need to show what we currently called Featured Foods til we get machine learning working
#Author: Leo Garcia
import home_page_connector as hp

class HomePage():
    def __init__(self, user_id):
        self.user_id = user_id
    
    def main_page(self):
        user_name = hp.HomePageConnector(self.user_id).get_user_name()
        rec_meals = hp.HomePageConnector(self.user_id).get_user_rec_meals()
        print("**********************")
        print("*      Home Page     *")
        print("**********************")
        print("Welcome,", user_name[0], user_name[1])
        self.display_recommended_meals(rec_meals)

    def display_recommended_meals(self, rec_meals):
        print("Todays recommened meals for you: ")
        print(rec_meals)

