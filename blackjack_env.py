from typing import List
from card import Card
from shoe import Shoe


class Actions:
    stay = 0
    hit = 1
    double = 2
    split = 3


class BlackJackEnv:
    def __init__(self, num_decks:int = 2):
        self.shoe = Shoe(num_decks=num_decks)
        self.user_hands = []
        self.current_hand_index = 0
        self.dealer_cards = []

        self.dealer_card_showing = 0
        self.has_usable_ace = False

    def reset(self):
        self.user_hands = [[self.shoe.deal_card(), self.shoe.deal_card()]]
        self.dealer_cards = [self.shoe.deal_card()]
        self.dealer_card_showing = self.dealer_cards[0].value
        return self.return_state()

    def step(self, action: int, bet: int = 1):
        current_hand = self.user_hands[self.current_hand_index]
        if self._calc_score() == 21:
            return self.return_state(), bet, True

        if action == Actions.hit:
            self.add_user_card()
            if self.is_bust():
                return self.return_state(), -bet, True
            else:
                return self.return_state(), 0, False
        elif action == Actions.stay:
            return self.deal_dealer(bet=bet)
        elif action == Actions.double:
            self.add_user_card()
            if self.is_bust():
                return self.return_state(), -2*bet, True
            else:
                return self.deal_dealer(bet=2*bet)

    def add_user_card(self) -> None:
        new_card = self.shoe.deal_card()
        self.user_hands[self.current_hand_index].append(new_card)

    def deal_dealer(self, bet: int = 1):
        while sum([card.value for card in self.dealer_cards]) < 17:
            dealer_card = self.shoe.deal_card()
            self.dealer_cards.append(dealer_card)

        dealer_card_sum = sum([card.value for card in self.dealer_cards])

        if self.is_bust(self.dealer_cards):
            return self.return_state(), bet, True
        elif dealer_card_sum > self._calc_score():
            return self.return_state(), -bet, True
        elif dealer_card_sum == self._calc_score():
            return self.return_state(), 0, True
        else:
            return self.return_state(), bet, True

    def return_state(self):
        return self._calc_score(), self.dealer_card_showing, self.has_usable_ace

    def _current_hand(self):
        return self.user_hands[self.current_hand_index]

    def _calc_score(self) -> int:
        # This is needed for ace logic
        # could make more efficient by checking for aces, but by then you're already iterating through the list
        # TODO maybe could keep track off all the aces in the hand in class vars but other things to do first

        current_hand = self._current_hand()
        total_sum = 0
        aces = []
        for card in current_hand:
            total_sum += card.value
            if card.rank == 'Ace':
                aces.append(card)

        final_ace_amount = len(aces)
        if total_sum > 21:
            for ace in aces:
                final_ace_amount -= 1
                ace.change_ace_value_to_one()
                total_sum -= 10
                if total_sum <= 21:
                    break

        if final_ace_amount > 0:
            self.has_usable_ace = True

        return total_sum

    @staticmethod
    def is_bust(cards):
        return sum([card.value for card in cards]) > 21
