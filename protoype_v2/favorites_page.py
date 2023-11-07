#Author Jack W.

import sqlite3

# Function to list favorite meals for a user
def list_favorite_meals(user_id):
    conn = sqlite3.connect("favorite_meals.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM favorite_meals WHERE user_id=?", (user_id,))
    favorite_meals = cursor.fetchall()

    conn.close()

    if favorite_meals:
        print("Your Favorite Meals:")
        for meal in favorite_meals:
            print(f"ID: {meal[0]}, Name: {meal[1]}, Description: {meal[2]}")
    else:
        print("You haven't added any meals to your favorites yet.")
        
    #Displays the different options a user can do like nothing or 
    #change account info     
    print("6. Home Page")
    print("8. Favorites Page")
    print("9. Account Page")
    print("0. Quit App")

    response = int(input("What would you like to do?\n"))
    
    #if the user chooses to change info, then gets new info from user
    if response == 1:
        pass
    elif (response in range(6,10)) or (response == 0):
        return(response)
        
    else:
        print(response)
        print("Your response didn't match the desired input. \nPlease choose one of the options above.")



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
