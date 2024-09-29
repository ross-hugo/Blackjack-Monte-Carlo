import numpy as np
from collections import defaultdict
from random import choice, random
from tqdm import tqdm
from blackjack_env import BlackJackEnv, Actions

class MonteCarlo:
    def __init__(self, num_decks: int = 1, alpha: float = 0.1, epsilon: float = 0.1):
        self.non_first_actions = [Actions.hit, Actions.stay]
        self.first_actions = self.non_first_actions + [Actions.double]
        self.bj_env = BlackJackEnv()
        self.alpha = alpha  # learning rate for incremental Q updates
        self.epsilon = epsilon  # epsilon for epsilon-greedy policy
        self.policy = defaultdict(lambda: np.zeros(len(self.first_actions)))  # policy table

    def simulate_episode(self):
        episode_results = []
        viable_actions = self.get_first_actions()
        is_first_turn = True
        state = self.bj_env.reset()
        while True:
            action = self.choose_action(state, is_first_turn)  # Use policy to choose action
            next_state, reward, done = self.bj_env.step(action)
            if is_first_turn:
                is_first_turn = False
                viable_actions = self.get_non_first_actions()
            episode_results.append((state, action, reward))
            state = next_state

            if done:
                break

        return episode_results

    def choose_action(self, state, is_first_turn):
        """Choose action based on epsilon-greedy policy"""
        if random() < self.epsilon:  # Exploration
            if is_first_turn:
                return choice(self.get_first_actions())
            else:
                return choice(self.get_non_first_actions())
        else:  # Exploitation
            action_values = self.policy[state]
            if is_first_turn:
                # First turn allows all actions (hit, stay, double)
                return np.argmax(action_values[:len(self.first_actions)])
            else:
                # Non-first turn actions (hit, stay)
                return np.argmax(action_values[:len(self.non_first_actions)])

    def exec(self, num_episodes: int = 1000, gamma: float = 1.0):
        Q = defaultdict(lambda: np.zeros(len(self.first_actions)))  # Action-value function
        N = defaultdict(lambda: np.zeros(len(self.first_actions)))  # State-action visit counts

        for _ in tqdm(range(num_episodes)):
            episode = self.simulate_episode()
            states, actions, rewards = zip(*episode)
            discounts = np.array([gamma ** i for i in range(len(rewards))])

            for i, state in enumerate(states):
                action = actions[i]
                G = sum(rewards[i:] * discounts[:len(rewards[i:])])  # Calculate return (G)
                N[state][action] += 1  # Count visits

                # Incremental mean formula for Q(s, a)
                Q[state][action] += self.alpha * (G - Q[state][action])  # Update Q with constant alpha

                # Update policy to be greedy w.r.t. Q
                self.policy[state] = Q[state]  # Greedy policy based on Q

        return Q

    def get_first_actions(self):
        return self.first_actions

    def get_non_first_actions(self):
        return self.non_first_actions


if __name__ == "__main__":
    mc = MonteCarlo(num_decks=6, alpha=0.1, epsilon=0.1)
    Q_values = mc.exec(num_episodes=1000, gamma=0.9)
    print(Q_values)
