from card import Card


class Actions:
    stay = 0
    hit = 1
    double = 2


class BlackJackEnv:
    def __init__(self, shoe):
        self.shoe = shoe
        self.user_cards = []
        self.dealer_cards = []

        self.user_card_sum = 0
        self.dealer_card_showing = 0
        self.has_usable_ace = False

    def reset(self):
        self.user_cards = [self.shoe.deal_card(), self.shoe.deal_card()]
        self.dealer_cards = [self.shoe.deal_card()]
        self.user_card_sum = sum([card.value for card in self.user_cards])
        self.dealer_card_showing = self.dealer_cards[0].value
        return self.return_state()

    def step(self, action: int, bet: int = 1):
        if self.user_card_sum == 21:
            return self.return_state(), bet, True

        if action == Actions.hit:
            self.add_user_card()
            if self.is_bust(self.user_cards):
                return self.return_state(), -bet, True
            else:
                return self.return_state(), 0, False
        elif action == Actions.stay:
            return self.deal_dealer(bet=bet)
        elif action == Actions.double:
            self.add_user_card()
            if self.is_bust(self.user_cards):
                return self.return_state(), -2*bet, True
            else:
                return self.deal_dealer(bet=2*bet)

    def add_user_card(self) -> None:
        new_card = self.shoe.deal_card()
        self.user_cards.append(new_card)
        self.user_card_sum = self._calc_score(self.user_cards)

    def deal_dealer(self, bet: int = 1):
        while sum([card.value for card in self.dealer_cards]) < 17:
            dealer_card = self.shoe.deal_card()
            self.dealer_cards.append(dealer_card)

        dealer_card_sum = sum([card.value for card in self.dealer_cards])

        if self.is_bust(self.dealer_cards):
            return self.return_state(), bet, True
        elif dealer_card_sum > self.user_card_sum:
            return self.return_state(), -bet, True
        elif dealer_card_sum == self.user_card_sum:
            return self.return_state(), 0, True
        else:
            return self.return_state(), bet, True

    def return_state(self):
        return self.user_card_sum, self.dealer_card_showing, self.has_usable_ace

    def _calc_score(self, cards: [Card]) -> int:
        # This is needed for ace logic
        # could make more efficient by checking for aces, but by then you're already iterating through the list
        # maybe could keep track off all the aces in the hand in class vars but other things to do first
        total_sum = 0
        aces = []
        for c in cards:
            total_sum += c.value
            if c.rank == 'Ace':
                aces.append(c)

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
