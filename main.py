from collections import defaultdict
from random import choice
import numpy as np
from shoe import Shoe
from tqdm import tqdm

# TODO add proper ace logic
# TODO look into multiprocessing because this will probably be a pretty beefy calculation
# TODO is this even possible in this implementation?
# TODO add card counting
# TODO add splits


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

    def reset(self):
        self.user_cards = [self.shoe.deal_card(), self.shoe.deal_card()]
        self.dealer_cards = [self.shoe.deal_card()]
        self.user_card_sum = sum([card.value for card in self.user_cards])
        self.dealer_card_showing = self.dealer_cards[0].value
        return self.user_card_sum, self.dealer_card_showing

    def step(self, action: int):
        if self.user_card_sum == 21:
            return self.return_state(), 1, True

        if action == Actions.hit:
            self.add_user_card()
            if self.is_bust(self.user_cards):
                return self.return_state(), -1, True
            else:
                return self.return_state(), 0, False
        elif action == Actions.stay:
            return self.deal_dealer(bet=1)
        elif action == Actions.double:
            self.add_user_card()
            if self.is_bust(self.user_cards):
                return self.return_state(), -2, True
            else:
                return self.deal_dealer(bet=2)

    def add_user_card(self) -> None:
        new_card = self.shoe.deal_card()
        self.user_cards.append(new_card)
        self.user_card_sum += new_card.value

    def deal_dealer(self, bet: int = 1):
        user_card_sum = sum([card.value for card in self.user_cards])
        while sum([card.value for card in self.dealer_cards]) < 17:
            dealer_card = self.shoe.deal_card()
            self.dealer_cards.append(dealer_card)

        dealer_card_sum = sum([card.value for card in self.dealer_cards])

        if self.is_bust(self.dealer_cards):
            return self.return_state(), bet, True
        elif dealer_card_sum > user_card_sum:
            return self.return_state(), -bet, True
        elif dealer_card_sum == user_card_sum:
            return self.return_state(), 0, True
        else:
            return self.return_state(), bet, True

    def return_state(self):
        return self.user_card_sum, self.dealer_card_showing

    @staticmethod
    def is_bust(cards):
        return sum([card.value for card in cards]) > 21


class MonteCarlo:
    def __init__(self, num_decks: int = 1):
        self.non_first_actions = [Actions.hit, Actions.stay]
        self.first_actions = self.non_first_actions + [Actions.double]
        bj_shoe = Shoe(num_decks=num_decks)
        self.bj_env = BlackJackEnv(shoe=bj_shoe)
        # TODO figure out how to deal with splits

    # TODO add card counting
    def exec(self, num_episodes: int = 1000, gamma: float = 1.0):
        returns_sum = defaultdict(lambda: np.zeros(len(self.first_actions)))
        Q = defaultdict(lambda: np.zeros(len(self.first_actions)))
        N = defaultdict(lambda: np.zeros(len(self.first_actions)))

        for _ in tqdm(range(num_episodes)):
            episode = self.simulate_episode()
            states, actions, rewards = zip(*episode)
            discounts = np.array([gamma ** i for i in range(len(rewards)+1)])
            for i, state in enumerate(states):
                N[state][actions[i]] += 1
                returns_sum[state][actions[i]] += sum(rewards[i:] * discounts[:-(1 + i)])
                Q[state][actions[i]] = returns_sum[state][actions[i]] / N[state][actions[i]]

        print(Q)
        return Q

    def simulate_episode(self):
        episode_results = []
        viable_actions = self.get_first_actions()
        is_first_turn = True
        state = self.bj_env.reset()
        while True:
            action = choice(viable_actions)
            next_state, reward, done = self.bj_env.step(action)
            if is_first_turn:
                is_first_turn = False
                viable_actions = self.get_non_first_actions()
            episode_results.append((state, action, reward))
            state = next_state

            if done:
                break

        return episode_results

    def get_first_actions(self):
        return self.first_actions

    def get_non_first_actions(self):
        return self.non_first_actions


if __name__ == "__main__":
    mc = MonteCarlo(num_decks=6)
    mc.exec(num_episodes=5000000, gamma=.9)
