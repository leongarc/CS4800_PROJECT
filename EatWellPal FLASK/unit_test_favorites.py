# Unit testing for favorites_db_connector
# By Leo Garcia
import unittest
from connectors import favorites_db_connector

class FavoritesDBConnTest(unittest.TestCase):
    def setUp(self):
        self.test_user = 555
        self.db = favorites_db_connector.FavoritesDBConnector(self.test_user)
        self.recipe = ["Pork Chops with Asparagus and a Lemon Sage Cream Sauce", 17]
        self.fake_recipe = 99999999999999

    def tearDown(self):
        self.db.delete_favorites(self.recipe[1])
        self.db.close_connection()
    
    # Should not return false since database exists
    def test_connect_to_db(self):
        self.assertIsNot(self.db.connect_to_db(), False)

    # Should be false since user_id 555 does not have favorites
    def test_get_favorites(self):
        self.assertFalse(self.db.get_favorites())

    # Test to see if inserted information returns none. It shouldn't
    def test_insert_favorite(self):
        self.db.insert_favorites(self.recipe[0], self.recipe[1])

        self.assertIsNotNone(self.db.get_favorites())
   
    # Test to see of delete_favs works
    def test_delete_favorite(self):
        self.db.insert_favorites(self.recipe[0], self.recipe[1])
        self.db.delete_favorites(self.recipe[1])

        self.assertIsNone(self.db.get_favorites())

    # Test for favorite exists. Inserts data into database and should return True
    def test_favorite_exists(self):
        self.db.insert_favorites(self.recipe[0], self.recipe[1])

        self.assertTrue(self.db.favorite_exists(self.recipe[1]))

    # Test for favorite exists. Should return false since recipe doesn't exist
    def test_favorite_exists_false(self):
        self.assertFalse(self.db.favorite_exists(self.recipe[1]))

    # Tests get recipe. Should return data not False
    def test_get_recipe(self):
        self.assertIsNot(self.db.get_recipe(str(self.recipe[1])), False)

    # Tests get recipe. Should return False since this recipe id does't exist.
    def test_get_recipe_false(self):
        self.assertFalse(self.db.get_recipe(str(self.fake_recipe)))