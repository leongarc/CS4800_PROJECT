#this is controller for the login page and for the account page
#connects the login command UI page to the database to pull the information needed

#Authors Luis and Uriel

import sqlite3
from flask_login import UserMixin


class AccountManagement(UserMixin):
    
    #initialize variables
    def __init__(self):
        self.conn = sqlite3.connect('database.db')
        self.cur = self.conn.cursor()
        
        
    def close_connection(self):
        self.conn.close()
        
    #checks to see if the username or email is already in use    
    def signup_check(self, username, email):
        res = self.cur.execute("SELECT username FROM users WHERE username = ? or email = ?", (username, email))
        username_check = res.fetchone()
        
        #returns True if the username or email exist, otherwise False
        return bool(username_check)
    
    #Create the new account for the user
    def create_account(self, username, email, password, fname, lname, body_weight, height, target_weight, allergies, gender):
        self.cur.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, password))
        self.cur.execute("SELECT user_id FROM users WHERE username = ? AND password = ?", (username, password))
        if int(target_weight) > int(body_weight):
            calorie_intake = (int(body_weight) * 15) + 500
        else:
            calorie_intake = (int(body_weight) * 15) - 500

        result = self.cur.fetchone()
        self.cur.execute("INSERT INTO userinfo (user_id, first_name, last_name, body_weight, height, goal, allergies, calorie_intake, Gender) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (result[0], fname, lname, body_weight, height, target_weight, allergies, calorie_intake, gender))
        self.conn.commit()
        
    #Authenticate the user by checking the username and password
    def login(self, username, password):
        self.cur.execute("SELECT user_id FROM users WHERE username = ? AND password = ?", (str(username), str(password)))
        result = self.cur.fetchone()
        
        #Returns the user_id if authentication is successful, else None
        return result[0] if result else None
    
    #Gets information about the user(For account page currently)
    def get_info(self, user_id):
        self.cur.execute("SELECT user_id, username, email FROM users WHERE user_id = ?", (str(user_id)))
        
        results = self.cur.fetchone()
        if results:
            user_object = AccountManagement()
            user_object.id = results[0]
            user_object.username = results[1]
            user_object.email = results[2]
        
            return user_object
        
        return None
    
    def about_user(self, user_id):
        self.cur.execute("SELECT first_name, last_name, body_weight, height, goal, allergies, calorie_intake FROM userinfo WHERE user_id = ?", (str(user_id)))
        results = self.cur.fetchone()
        if results: 
            
            return results
        else:
            results = None
            return results

    #A method to update the information for the user
    def update_info(self, userid, fname, lname, bweight, height, goal, allergies, gender):
        if int(goal) > int(bweight):
            calorie_intake = (int(bweight) * 15) + 500
        else:
            calorie_intake = (int(bweight) * 15) - 500

        self.cur.execute("UPDATE userinfo\
                        SET first_name = ?,\
                            last_name = ?,\
                            body_weight = ?,\
                            height = ?,\
                            goal = ?,\
                            allergies = ?,\
                            calorie_intake = ?,\
                            gender = ?\
                        WHERE user_id = ?", (fname, lname, bweight, height, goal, allergies, calorie_intake, gender, str(userid)))
        self.conn.commit()


    def delete_account(self, user_id):
        self.cur.execute("DELETE FROM users\
            WHERE user_id = ?", (str(user_id)))
        self.cur.execute("DELETE FROM userinfo\
            WHERE user_id = ?", (str(user_id)))
        
        self.conn.commit()

    def username(self, user_id):
        self.cur.execute("SELECT first_name, last_name FROM userinfo WHERE user_id = ?", (str(user_id)))
        results = self.cur.fetchone()
        if results: 
            name_info = [result for result in results]
            user_name = '  '.join(name_info)
            return user_name
        else:
            results = None
            return results