from card import Card
from random import shuffle, choice


class Shoe:
    def __init__(self, num_decks: int = 1) -> None:
        self.cards = []
        self.num_decks = num_decks
        self.all_suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        self.all_ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']

        self.generate_shoe()

    def generate_shoe(self) -> None:
        self.cards = [
            Card(suit, rank) for _ in range(self.num_decks) for suit in self.all_suits for rank in self.all_ranks
        ]

    def shuffle_shoe(self) -> None:
        shuffle(self.cards)

    def deal_card(self) -> Card:
        if len(self.cards) > 0:
            return self.cards.pop(0)
        else:
            self.generate_shoe()
            self.shuffle_shoe()
            return self.deal_card()

    def random_card(self) -> Card:
        if self.cards:
            return choice(self.cards)
        self.generate_shoe()
        self.random_card()

    def pure_random_card(self) -> Card:
        return Card(suit=choice(self.all_suits), rank=choice(self.all_ranks))
