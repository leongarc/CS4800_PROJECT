import account_page as ap
import favorites_page
import home_page as hp
import login

if __name__ == "__main__":
    user_id = login.login()

    #hp.HomePage(user_id).main_page()
    
    while(user_id != None):
        ap.account_page(user_id)
    
    