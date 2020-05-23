# Importing Unit Testing Module
import unittest

# Importing functions which need to be tested
from function_test import check_input_b

class TestMethods(unittest.TestCase):
    
    def test_input_players(self):
        self.assertRaises(ValueError, check_input_b, -1, 1, 1)
        
    def test_input_decks(self):
        self.assertRaises(ValueError, check_input_b, 1, 0, 1)
        
    def test_input_decision(self):
        self.assertRaises(ValueError, check_input_b, 1, 1, 2)
        
if __name__ == '__main__':
    unittest.main()

