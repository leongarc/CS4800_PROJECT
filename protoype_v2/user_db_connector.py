#this is controller for the login page and for the account page
#connects the login command UI page to the database to pull the information needed

#Authors Luis and Uriel

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


def create_account(username, email, password, fname, lname, body_weight, height, target_weight, allergies, calorie_intake, gender):
    #makes the connection the the Users Database
    con = sqlite3.connect("users.db")

    #Creates the Cursor to be able to work in the database
    cur = con.cursor()

    cur.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, password))
    cur.execute("SELECT user_id FROM users WHERE username = ? AND password = ?", (username, password))
    result = cur.fetchone()
    cur.execute("INSERT INTO userinfo (user_id, first_name, last_name, body_weight, height, goal, allergies, calorie_intake, Gender) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (result[0], fname, lname, body_weight, height, target_weight, allergies, calorie_intake, gender))
    con.commit()



#Create a login function to authenticate users
def login(username, password):
    user_conn = sqlite3.connect("users.db")
    user_cursor = user_conn.cursor()
    user_cursor.execute("SELECT user_id FROM users WHERE username = ? AND password = ?", (username, password))
    
    result = user_cursor.fetchone()
    
    user_conn.close()
    return result[0] if result else None


#gets all the info from logged in user
def get_info(user_id):
    user_conn = sqlite3.connect("users.db")
    user_cursor = user_conn.cursor()
    user_cursor.execute("SELECT first_name, last_name, body_weight, height, goal, allergies FROM userinfo WHERE user_id = ?", (str(user_id)))
    
    results = user_cursor.fetchone()
    return(results)

#fucntion to change info from the database for logged in user
def update_info(userid, fname, lname, bweight, height, goal, allergies):
    user_conn = sqlite3.connect("users.db")
    user_cursor = user_conn.cursor()
    user_cursor.execute("UPDATE userinfo\
                        SET first_name = ?,\
                            last_name = ?,\
                            body_weight = ?,\
                            height = ?,\
                            goal = ?,\
                            allergies = ?\
                        WHERE user_id = ?", (fname, lname, bweight, height, goal, allergies, str(userid)))
    user_conn.commit()


