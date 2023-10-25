import login_db_connector as log
import os    
os.chdir(os.path.dirname(os.path.abspath(__file__)))


if __name__ == "__main__":
    while True:
        print("**************************")
        print("* Welcome to Eat Well Pal*")
        print("**************************")
        print("1. Sign up")
        print("2. Login")
        print("3. Exit")

        answer = input("Enter your choice: ")
        if answer == "1":
            username = input("Username: ")
            email = input("Email: ")
            password = input("Password: ")
            check = log.signup_check(username, email)
            if check == True: 
                print("*****Username or Email already in use, try logging in*****")
            else:
                fname = input("What is your first name: ")
                lname = input("What is your last name: ")
                body_weight = input("What is your current body weight(in pounds): ")
                height = input("What is your current height(ft, in): ")
                target_weight = input("What is your target weight: ")
                allergies = input("Do you have any allergies: ")
                # calculate daily calorie intake
                if target_weight > body_weight:
                    calorie_intake = (body_weight * 15) + 500
                else:
                    calorie_intake = (body_weight * 15) - 500
                log.create_account(username, email, password, fname, lname, body_weight, height, target_weight, allergies, calorie_intake)


                break
        elif answer == "2":
            username = input("Enter your username: ")
            password = input("Enter your password: ")

            # Attempt to log in
            user_id = log.login(username, password)

        elif answer == "3":
            break
        #add the function that leads to home page