from flask import Flask, render_template, url_for, request, redirect
import sqlite3
from connectors import user_db_connector as user
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin

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
            print(type(user_id))
            user_obj = users.get_info(user_id)
            login_user(user_obj)  # Log in the user
            return redirect(url_for('main'))  # Redirect to a dashboard or profile page

    return render_template('login.html', error='Invalid username or password')



#a way to log out, login is required
@app.route('/logout')
@login_required
def logout():
    logout_user()  # Log out the user
    return redirect(url_for('home'))  # Redirect to your home page

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


#temp dashboard to test login feature
@app.route('/main')
@login_required
def main():
    username=current_user.username
    return render_template('main.html', username=username)

@app.route('/meals')
@login_required
def meals():
    return render_template('meals.html')

@app.route('/progress')
@login_required
def progress():
    return render_template('progress.html')

@app.route('/favorites')
@login_required
def favorites():
    return render_template('favorites.html')


@app.route('/account')
@login_required
def account():

    log_user = user.AccountManagement()
    log_user = log_user.about_user(current_user.id)



    return render_template('account.html', log_user = log_user)


if __name__ == '__main__':
    app.run(debug=True)