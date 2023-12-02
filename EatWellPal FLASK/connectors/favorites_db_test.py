# Test for favorites_db_connector.py
# By Leo Garcia
import favorites_db_connector
def main():
    fav = favorites_db_connector.FavoritesDBConnector()
    data = fav.get_favorites(2)
    print(fav)
if __name__ == "__main__":
    main()