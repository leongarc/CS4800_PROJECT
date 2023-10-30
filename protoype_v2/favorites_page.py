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

def main():
    # Get user input (user ID or username)
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    # Authenticate the user and get their user_id
    user_id = login(username, password)

    if user_id is not None:
        # List favorite meals for the authenticated user
        list_favorite_meals(user_id)
    else:
        print("Invalid username or password. Please try again.")

# Include the signup_check, login, and other functions from the reference code

if __name__ == "__main__":
    main()
