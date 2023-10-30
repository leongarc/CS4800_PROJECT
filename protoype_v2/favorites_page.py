#This page will hold the command line UI for the favorites page
#displaying meals that were favorited by the user
import sqlite3

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
    user_id = input("Enter your user ID: ")

    try:
        user_id = int(user_id)
    except ValueError:
        print("Invalid user ID. Please enter a valid user ID.")
        return

    list_favorite_meals(user_id)

if __name__ == "__main__":
    main()

#jack w
