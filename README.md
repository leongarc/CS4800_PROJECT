# README for EatWellPal

## Description
The primary challenge for many individuals when managing their weight is not just monitoring calorie intake for gaining or losing weight, but rather the difficulty of maintaining a clear understanding of their goals and finding suitable meals that align with their dietary plans. This issue is further emphasized by the struggle to discover meals that conform to a prescribed plan and accommodate specific dietary restrictions. Many existing calorie counter and diet apps fall short in this regard as they primarily focus on tracking calories and meeting daily targets without offering comprehensive meal suggestions that fit within a user's calorie and dietary requirements. EatWellPal is an application that provides the calorie content of individual ingredients and offers complete meal suggestions tailored to a user's specific calorie and nutritional objectives.

## Configuration
See requirements.txt

## Usage
1) Head over to EatWellPal FLASK directory
2) Run main.py to start app
3) Go to browser of choice and in the URL enter 127.0.0.1:5000
4) Login or create an account
5) After logging in or signing up, you'll reach the Home Page
6) This is your main page where you can navigate to account settings, Calorie Tracker, Favorites, and Progress Page. This page also shows your recommened meals for the day.

Calorie Tracker: You'll be prompted to enter the name of the meal plus the weight. Calories are then automatically calculated and added into your calorie intake progress.

Favorites: Simply a page to see your favortied meals.

Progress Page: Simply a page where you can see you calorie consumption progress, illustated in a graph.

## Files
### Connectors:
	Favorites_db_connector.py - Has code that communicates with the database.db, favorites meals table, as well as the calorie intake table. Retrieves favorites, inserts favorites, and inserts consumed meals into the database.
	Favorties_db_test.py - Code to test the functionality of the favorites_db_connector.py while developing.
	Progress_connector.py - has the code that connects the progress page to the db  
	RecomendedMeal.py - Has all the machine learning code along with additional functionality for main and meals page 
	User_db_connector.py- Has the logic to authenticate users for login, logic to create new users, return user info for all pages and account page. 
### Static 
	Images – Source for the burger image and favicons 
### Styles 
	Accounts.css - styling for account page 
	Favorties_style.css - Has styling for the favorites page as well as two JavaScript scripts. Scripts handle populating the horizontal list slider with favorites and deletes the button when a favorite is deleted. 
	Login_style.css - page controls the css for the login as well as the signup and additional info pages as they are similar 
	Progress_styles.css 
	Style.css - Has styling code for the menu for the entirety of EatWellPal web app. 
### Templates 
	Account.html - html code to display the account page 
	Addintake.html - for testing, not in use 
	Additional_info.html - html code to get additional information to finish signup 
	Calorie_progree.html - for testing, not in use 
	Delete_account.html - html to make sure user wants to delete account 
	Edit_account.html - page to get info to update account 
	Favoirtes.html - html code to display list of meals in user favorite 
	Home.html - home page that links login and signup page 
	Login.html - html code to display login  
	Main.html - html code that displays machine learning results 
	Meals.html - html code that runs our meal search function 
	Meal_data.html - html code to diplay meal information, from clicking on meals from main or meals 
	Progress.html- html code that displays your progress on the progress page 
	Signup.html - page controls the HTML for signup  page.  This page controls getting basic info like email and password and returning it to main.py 
	Weight_progress.html -html code that displays your weight progress on the progress page 
### Main
    Database.db - holds all data in separate tables 
    Main.py - has all app.routes to connect python to html 
    Progress_unit_test.py- unit test for the progress page 
    Requirements.txt - Has all the dependencies for EatWellPal listed for ease of installation. 
    Unit_test_user_db.py - Unit test the user_db_connector 
    Unit_test_favorites.py - Unit testing for favorites_db_connector.py 
    Unit_test_recomended.py - unit testing for my recomendedMeal

### Test Accounts
	username- 'fa' password - 'fa'
	username- 'ba' password - 'ba'
	username- 'test' password - 'test'

## Features
Calorie Tracker - Track your calories

Favorite Meals Page - You could have your collection of favorte meals are here

Progress Page - This is where you'll find your weight progress. You can see where you stand depending on the meals you’ve eaten and your weight progression.

Home Page - Recommend a list of meals to eat to satisfy Daily Calorie intake using TF-IDF, and other methods

## Roadmap
EatWellPal end goal is to provide personalized meal suggestions via machine learning. 

## Acknowledgments
Dev Team: Uriel Alvarez, Luis Ochoa, Jack Wheeland, Leo Garcia

## Contact
do-not-reply@eatwellpal.com

## Changelog
Beta Ver. 1.0 -- Switching over to Flask
