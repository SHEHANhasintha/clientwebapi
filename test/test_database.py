import unittest
import sys
sys.path.insert(1, sys.path.append('../'))

from database.dataBase import Database

class TestDatabase(unittest.TestCase):
    def test_connection(self):
        self.db = Database()
        #self.db.getDatabase()
        #print(self.db)
        self.assertEqual(self.db.getDatabase(),122)


    """def test_get(self):

    def test_post(self):

    def test_update(self):

    def test_delete(self):

    """