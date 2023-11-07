#This page will hold the command line UI for the home page
#This page will need to show the Username or First and Last name
#This page will need to show what we currently called Featured Foods til we get machine learning working
#Author: Leo Garcia
import home_page_connector as hp
import os

class HomePage():
    def __init__(self, user_id):
        self.user_id = user_id
    
    def main_page(self):
        os.system('clear')
        user_name = hp.HomePageConnector(self.user_id).get_user_name()
        rec_meals = hp.HomePageConnector(self.user_id).get_user_rec_meals()
        print("**********************")
        print("*      Home Page     *")
        print("**********************")
        print("Welcome,", user_name[0], user_name[1])
        self.display_recommended_meals(rec_meals)
        
        print("7. Progress Page")
        print("8. Favorites Page")
        print("9. Account Page")
        print("0. Quit App")

        response = int(input("What would you like to do?\n"))
        
        if response == 1:
            pass
        
        elif (response in range(6,10)) or (response == 0):
            return(response)

    def display_recommended_meals(self, rec_meals):
        print("Todays recommened meals for you: ")
        print(rec_meals)
        
        
#Add a function that lets the user choose if they want to add one of the recommended meals 
#Or they want to switch tabs ie Progress, Account, Favorite or sign out/quit application
#Have them return their response to the main page
#6. Home, 7. Progress, 8. Favorite, 9. Account, 0. Quit
