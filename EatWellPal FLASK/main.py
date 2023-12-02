#Authors: Everyone

from flask import Flask, render_template, url_for, request, redirect, flash
from connectors import user_db_connector as user
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from connectors import recomendedMeal
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

login_manager = LoginManager(app)

#sets the login view route
login_manager.login_view = 'login'

#This is a callback function to get info about logged in users in the session
@login_manager.user_loader
def load_user(user_id):
    return user.AccountManagement().get_info(int(user_id))

@app.route('/')
def home():
    return render_template('home.html')


#Logic behind the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Check the username and password
        username = request.form['username']
        password = request.form['password']
    
        users = user.AccountManagement()
        user_id = users.login(username, password)

        if user_id:
          #uses flask functions to handle login in a user for a session
            print(type(user_id))
            user_obj = users.get_info(user_id)
            login_user(user_obj)  # Log in the user
            return redirect(url_for('main'))  # Redirect to a dashboard or profile page

        flash('Login Error: Invaldid Username or Password')


    return render_template('login.html')


#logic to log in a user
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Get user input from the form
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Check if the username or email is already in use
        users = user.AccountManagement()
        if users.signup_check(username, email):
            return render_template('signup.html', error='Username or email is already in use.')

        # If not in use, proceed to the next step
        return render_template('additional_info.html', username=username, email=email, password=password)

    # If it's a GET request, render the signup form
    return render_template('signup.html', error=None)


#After we have verified that their username/email is not in use we get the rest of the info
@app.route('/complete_signup', methods=['POST'])
def complete_signup():
    # Retrieve user input from the additional_info form
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    fname = request.form['fname']
    lname = request.form['lname']
    body_weight = request.form['body_weight']
    height = request.form['height']
    target_weight = request.form['target_weight']
    allergies = request.form['allergies']
    gender = request.form['gender']

    # Create an instance of the User class
    users = user.AccountManagement()

    # Call the create_account method to store the additional information
    users.create_account(username, email, password, fname, lname, body_weight, height, target_weight, allergies, gender)

    # Close the database connection
    users.close_connection()

    # Redirect to a success page or another route
    return redirect(url_for('login'))

#All pages beyond require a user to be logged in except for login that is above.
#temp dashboard to test login feature
#a way to log out, login is required
@app.route('/logout')
@login_required
def logout():
    logout_user()  # Log out the user
    return redirect(url_for('home'))  # Redirect to your home page

@app.route('/account', methods = ['GET', 'POST'])
@login_required
def account():
    #gets information about the logged in user
    log_user = user.AccountManagement()
    log_user = log_user.about_user(current_user.id)
    if request.method == 'POST':
        return render_template('edit_account', user_id = current_user.id)

    return render_template('account.html', log_user = log_user)

@app.route('/edit_account', methods=['GET', 'POST'])
@login_required
def edit_account():
    if request.method=='POST':
        #user_id = request.form['user_id']
        fname = request.form['fname']
        lname = request.form['lname']
        body_weight = request.form['body_weight']
        height = request.form['height']
        target_weight = request.form['target_weight']
        allergies = request.form['allergies']
        gender = request.form['gender']

        # Create an instance of the User class
        users = user.AccountManagement()

        # Call the create_account method to store the additional information
        users.update_info(current_user.id ,fname, lname, body_weight, height, target_weight, allergies, gender)

        # Close the database connection
        users.close_connection()
        return redirect(url_for('account'))
    
    #When the user first goes to this screen, this will be returned since nothing is entered
    #in the page thus the method is GET
    return render_template('edit_account.html')

    
@app.route('/main', methods=['GET', 'POST'])
@login_required
def main():
    log_user = user.AccountManagement()
    log_user = log_user.about_user(current_user.id)

    if log_user is not None:
        # Create an instance of MealConnector
        tracker = recomendedMeal.MealConnector("database.db")

        # Process meal data, initialize TF-IDF, and get recommendations
        tracker.process_meal_data()

        # Render results template
        return render_template('main.html',
                                log_user=log_user,
                                user_input=tracker.get_ingredients(),
                                group_input=tracker.get_ingredients_group(),
                                recommendations_user=tracker.get_recommendations(tracker.get_ingredients(), None),
                                recommendations_group=tracker.get_recommendations(tracker.get_ingredients_group(), None),
                                new_meals=tracker.new_meals())
    else:
        return render_template('index.html', message="Login failed. Please check your credentials.")

    
@app.route('/meals_data/<string:recommendation_id>')
@login_required
def meals_data(recommendation_id):
    tracker = recomendedMeal.MealConnector("database.db")

    return render_template('meals_data.html', 
                           recipe_Name=tracker.get_meal_data_by_column(recommendation_id, 'RecipeName'),
                           recipe_Description=tracker.get_meal_data_by_column(recommendation_id, 'Description'),
                           recipe_Instructions=tracker.get_meal_data_by_column(recommendation_id, 'instruction'),
                           recipe_Ingredients=tracker.get_meal_data_by_column(recommendation_id, 'ingredients'),
                           recipe_Calories=tracker.get_meal_data_by_column(recommendation_id, 'Calories'),
                           recipe_ServingSize=tracker.get_meal_data_by_column(recommendation_id, 'ServingSize'),
                           recipe_CookTime=tracker.get_meal_data_by_column(recommendation_id, 'CookTime'),
                           recipe_PrepTime=tracker.get_meal_data_by_column(recommendation_id, 'PrepTime'),
                           )


@app.route('/progress')
@login_required
def progress():
    return render_template('progress.html')

@app.route('/favorites')
@login_required
def favorites():
    return render_template('favorites.html')

@app.route('/meals')
@login_required
def meals():
    return render_template('meals.html')

@app.route('/add_to_intake/<string:recipe_Name>', methods=['POST'])
def add_to_intake(recipe_Name):
    if request.method == 'POST':
        recipe_id = request.form.get('recipe_id')
        serving_ate = request.form.get('servingSize')
        tracker = recomendedMeal.MealConnector("database.db")

        serving_size = tracker.get_meal_data_by_column(recipe_Name, 'ServingSize')
        recipe_calories = tracker.get_meal_data_by_column(recipe_Name, 'Calories')
        user_id = current_user.id 
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 

        calories_ate = serving_ate * (recipe_calories/serving_size)

        tracker.add_meal_intake(recipe_Name,user_id,serving_ate,calories_ate,time)

        return redirect(url_for('recipe_details', recipe_id=recipe_id))

    return "Invalid Request", 400

if __name__ == '__main__':
    app.run(debug=True)
