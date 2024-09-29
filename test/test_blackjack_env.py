import unittest
from unittest.mock import patch
from card import Card
from blackjack_env import BlackJackEnv

class TestBlackJackEnv(unittest.TestCase):
    @patch('blackjack_env.Shoe.deal_card')
    def test_setup(self, mock_deal_card):
        mock_deal_card.side_effect = [
            Card('Hearts', '5'),  
            Card('Diamonds', 'Jack'),  
            Card('Spades', '7')  
        ]

        env = BlackJackEnv(num_decks=1)
        state = env.reset()

        self.assertEqual(state, (15, 7, False))
        
