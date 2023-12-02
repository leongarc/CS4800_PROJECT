# Test for favorites_db_connector.py
# By Leo Garcia
import favorites_db_connector
def main():
    data = [124,234]
    fav = favorites_db_connector.FavoritesDBConnector(2)
    fav.update_favorties(data)
    data = fav.get_favorites()
    print(data, "Hello")
if __name__ == "__main__":
    main()