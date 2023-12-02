# Test for favorites_db_connector.py
# By Leo Garcia
import favorites_db_connector
def main():
    data = [111,999,456,222,777,3456]
    user_id = 2
    fav = favorites_db_connector.FavoritesDBConnector(user_id)
    fav.update_favorties(data)
    data = fav.get_favorites()
    print(data, "Hello")
if __name__ == "__main__":
    main()