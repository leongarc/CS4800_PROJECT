# Test for favorites_db_connector.py
# By Leo Garcia
import favorites_db_connector
def main():

    user_id = 4
    fav = favorites_db_connector.FavoritesDBConnector(user_id)
    # fav.insert_favorites("Pork Chops with Asparagus and a Lemon Sage Cream Sauce", 17)
    # fav.insert_favorites("Mushroom Mac and Cheese", 27)
    data = fav.get_favorites()
    print(data)
if __name__ == "__main__":
    main()