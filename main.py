from collections import defaultdict
from random import choice
import numpy as np
from shoe import Shoe
from tqdm import tqdm
from blackjack_env import BlackJackEnv, Actions

# TODO add incremental mean when calculating Q
#   TODO add constant alpha for incremental mean
# TODO add policy table creation and usage instead of random choice
# TODO look into multiprocessing because this will probably be a pretty beefy calculation
# TODO add graph or visualization of resulting policy
# TODO add card counting
# TODO add splits


class MonteCarlo:
    def __init__(self, num_decks: int = 1):
        self.non_first_actions = [Actions.hit, Actions.stay]
        self.first_actions = self.non_first_actions + [Actions.double]
        bj_shoe = Shoe(num_decks=num_decks)
        bj_shoe.shuffle_shoe()
        self.bj_env = BlackJackEnv(shoe=bj_shoe)

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

        return Q

    def get_first_actions(self):
        return self.first_actions

    def get_non_first_actions(self):
        return self.non_first_actions


if __name__ == "__main__":
    mc = MonteCarlo(num_decks=6)
    mc.exec(num_episodes=20, gamma=.9)
