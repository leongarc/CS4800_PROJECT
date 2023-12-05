# Test for favorites_db_connector.py
# By Leo Garcia
import favorites_db_connector
def main():

    user_id_test1 = 4
    fav1 = favorites_db_connector.FavoritesDBConnector(user_id_test1)
    fav1.insert_favorites("Pork Chops with Asparagus and a Lemon Sage Cream Sauce", 17)
    fav1.insert_favorites("Mushroom Mac and Cheese", 27)
    data1 = fav1.get_favorites()
    print(data1)
   
    # Delete Test
    fav1.delete_favorites(27)
    data1 = fav1.get_favorites()
    print(data1)

    #Test for 'None' result
    user_id_test2 = 2
    fav2 = favorites_db_connector.FavoritesDBConnector(user_id_test2)
    data2 = fav2.get_favorites()
    if data2 is None:
        print("You have no favorites added.")
    else:
        print(data2)

if __name__ == "__main__":
    main()