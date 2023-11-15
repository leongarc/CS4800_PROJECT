#Author Jack W.

import sqlite3
import os

import sqlite3
import os

class FavoriteMealsPage:
    def __init__(self, user_id):
        self.user_id = user_id

    def list_favorite_meals(self):
        conn = sqlite3.connect("calorie_intake.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Favorite_meals WHERE user_id=?", (self.user_id,))
        favorite_meals = cursor.fetchall()

        conn.close()
        os.system('clear')
        print("*********************************")
        print("*         Eat Well Pall         *")
        print("*         Favorites Page        *")
        print("********************************* \n\n")

        if favorite_meals:
            print("Your Favorite Meals:")
            for meal in favorite_meals:
                print(f"ID: {meal[0]}, Name: {meal[1]}, Description: {meal[2]}")
        else:
            print("You haven't added any meals to your favorites yet.")
        
        # Display the different options a user can do like nothing or change account info     
        print("6. Home Page")
        print("9. Account Page")
        print("0. Quit App")

        response = int(input("What would you like to do?\n"))

        if response == 1:
            pass
        elif (response in range(6, 10)) or (response == 0):
            return response
        else:
            print(response)
            print("Your response didn't match the desired input. \nPlease choose one of the options above.")

if __name__ == "__main__":
    user_id = input("Enter your user ID: ")

    try:
        user_id = int(user_id)
    except ValueError:
        print("Invalid user ID. Please enter a valid user ID.")
    else:
        favorites_page = FavoriteMealsPage(user_id)
        while True:
            response = favorites_page.list_favorite_meals()
            if response == 0:
                break
            elif response == 6:
                # Handle Home Page
                pass
            elif response == 9:
                # Handle Account Page
                pass




# def main():
#     # Get user input (user ID or username)
#     username = input("Enter your username: ")
#     password = input("Enter your password: ")

#     # Authenticate the user and get their user_id
#     user_id = login(username, password)

#     if user_id is not None:
#         # List favorite meals for the authenticated user
#         list_favorite_meals(user_id)
#     else:
#         print("Invalid username or password. Please try again.")

# # Include the signup_check, login, and other functions from the reference code

# if __name__ == "__main__":
#     main()

#A function that ask the user if they want to switch tabs ie Progress, Account, Favorite or sign out/quit application
#Have their response return  to the main page
#6. Home, 7. Progress, 8. Favorite, 9. Account, 0. Quit
