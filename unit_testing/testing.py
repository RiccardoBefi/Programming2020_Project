# Importing Unit Testing Module
import unittest

# Importing functions which need to be tested
from function_test import check_input_blackjack, deck, listed, draw


class TestMethods(unittest.TestCase):
    
    def test_input_players(self):
        self.assertRaises(ValueError, check_input_blackjack, -1, 1)
        
    def test_input_decks(self):
        self.assertRaises(ValueError, check_input_blackjack, 1, 0)
        
    def test_deck(self):
        self.assertEqual(deck()[0], 0)
        
    def test_listed(self):
        self.assertEqual(listed()[0,0], '1')
        self.assertEqual(listed()[0,1], 'Hearts')
        
    def test_draw(self):
        # checking that the length of the deck is reduced by one
        self.assertEqual(len(draw()[1]), 51) 
        
        # checking that the first element of the deck is removed
        self.assertNotEqual(draw()[1][0], 0)
        
        #checking the new first element of the deck
        self.assertEqual(draw()[1][0], 1)
        
        
if __name__ == '__main__':
    unittest.main()
