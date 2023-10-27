#this is controller for the login page and for the account page
#connects the login command UI page to the database to pull the information needed

import sqlite3


def signup_check(username, email):


    #makes the connection the the Users Database
    con = sqlite3.connect("users.db")

    #Creates the Cursor to be able to work in the database
    cur = con.cursor()

    res = cur.execute("SELECT username FROM users WHERE username = ? or email = ?", (username, email))
    try: 
        username_check = res.fetchone()
    except: 
        username_check = None

    if username_check != None:
        return True
    else:
        return False


def create_account(username, email, password, fname, lname, body_weight, height, target_weight, allergies):
    #makes the connection the the Users Database
    con = sqlite3.connect("users.db")

    #Creates the Cursor to be able to work in the database
    cur = con.cursor()

    cur.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, password))
    cur.execute("SELECT user_id FROM users WHERE username = ? AND password = ?", (username, password))
    result = cur.fetchone()
    cur.execute("INSERT INTO userinfo (user_id, first_name, last_name, body_weight, height, goal, allergies) VALUES (?, ?, ?, ?, ?, ?, ?)", (result[0], fname, lname, body_weight, height, target_weight, allergies))
    con.commit()



#Create a login function to authenticate users
def login(username, password, fname, lname, body_weight, height, target_weight, allergies):
    user_conn = sqlite3.connect("users.db")
    user_cursor = user_conn.cursor()
    user_cursor.execute("SELECT user_id FROM users WHERE username = ? AND password = ?", (username, password))
    
    result = user_cursor.fetchone()
    
    user_conn.close()
    return result[0] if result else None

