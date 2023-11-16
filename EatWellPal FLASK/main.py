from flask import Flask, render_template, url_for, request, redirect
import sqlite3
from connectors import user_db_connector as user

app = Flask(__name__)

  


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

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


if __name__ == '__main__':
    app.run(debug=True)