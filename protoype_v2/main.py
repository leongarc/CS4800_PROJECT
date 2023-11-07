import account_page as ap
import favorites_page as fp
import home_page as hp
import progress_page as pp
import login

if __name__ == "__main__":
    user_id = login.login()

    page = 6
    #hp.HomePage(user_id).main_page()
    if user_id != None:
        while(page != None):

            #Home Page
            if page == 6:
                page = hp.HomePage(user_id).main_page()
            #Progress Page
            elif page == 7:
                page = pp.main(user_id)
            #Favorites
            elif page == 8:
                page = fp.list_favorite_meals(user_id)
            #Account
            elif page == 9:
                page = ap.account_page(user_id)     
            #Quit    
            elif page == 0:
                break

    
    