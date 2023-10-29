#This page will hold the command line UI for the account page
#this should display basic information about hte user like name, weight, height and allergies
#their should also be way for them to edit their account if they would like
#Author: Luis Ochoa

import user_db_connector as log

#function to display Account Page (command line UI version) 
def account_page(user_id):
    user_id = user_id
    print("*********************************")
    print("*         Eat Well Pall         *")
    print("*          Account Page         *")
    print("********************************* \n\n")
    
    #Gets the logged in user's info
    results = log.get_info(user_id)

    #Displays the logged in user's info
    print("First Name: ", results[0])
    print("Last Name: ", results[1])
    print("Body Weight: ", results[2])
    print("Height: ", results[3])
    print("Goal: ", results[4])
    print("Allergies: ", results[5])      
    
    #Displays the different options a user can do like nothing or 
    #change account info      
    response = input("Would you like to edit your account [Y]es or [N]o?\n")
    
    #if the user chooses to change info, then gets new info from user
    if response.upper() == "Y":
        fname = input("First Name: ")
        lname = input("Last Name: ")
        bweight = input("Body Weight: ")
        height = input("Height: ")
        goal = input("Goal: ")
        allergies = input("Allergies: ")
        
        log.update_info(user_id, fname, lname, bweight, height, goal, allergies)
    
    elif response.upper() == "N":
        pass
    
    else:
        print("Your response didn't match the desired input.  Input\
            [Y] for yes or [N] for no.")
    
    