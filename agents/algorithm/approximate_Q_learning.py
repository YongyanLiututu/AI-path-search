from template import Agent
import random, time, json
from Splendor.splendor_model import SplendorGameRule


class myAgent(Agent):
    def __init__(self, _id):
        super().__init__(_id)
        self.alpha = 0.01  # Learning rate parameter

    # Extract features function to derive features from game state and action
    def extract_features(self, state, action):
        current_game_board = state.board  # Get the current game board state
        current_agent = state.agents[self.id]  # Get the current agent's state
        game_features_list = []  # Initialize the game features list
        self.get_three_tier_features(action, current_agent, current_game_board, game_features_list)
        self.buy_action_feature(action, current_game_board, game_features_list)
        return game_features_list

    # Process features for a buy action
    def buy_action_feature(self, action, current_game_board, game_features_list):
        if 'buy' in action['type']:  # Check if the action is a buy action
            card = self.get_card_point_feature(action, game_features_list)
            self.get_card_cost_feature(card, game_features_list)
            self.get_noble_demand_gem_feature(card, current_game_board, game_features_list)
        else:  # If not a buy action, append zeros to the features list
            game_features_list.extend([0] * 3)

    # Process features related to noble demand for gems
    def get_noble_demand_gem_feature(self, card, current_game_board, game_features_list):
        min_noble_demand = 0
        max_noble_demand = 12
        noble_needed = 0
        for noble in current_game_board.nobles:
            if card.colour in noble[1]:
                noble_needed += 1
        normalized_noble_needed = (noble_needed - min_noble_demand) / (max_noble_demand - min_noble_demand)
        game_features_list.append(normalized_noble_needed)

    # Process features related to card cost
    def get_card_cost_feature(self, card, game_features_list):
        total_cost = sum(card.cost.values())
        game_features_list.append(total_cost / 10)

    # Process features related to card points
    def get_card_point_feature(self, action, game_features_list):
        card = action['card']
        game_features_list.append(card.points / 10)
        return card

    # Process features related to collecting gems across three tiers card
    def get_three_tier_features(self, action, current_agent, current_game_board, game_features_list):
        if 'collect' in action['type']:  # Check if the action is a collect action
            for tier in range(3):
                if current_game_board.dealt[tier] is not None and tier == 0:  # Only consider level 1 cards
                    color_needed = {'black': 0, 'red': 0, 'green': 0, 'blue': 0, 'white': 0, 'yellow': 10}
                    for card in current_game_board.dealt[tier]:
                        if card and card.cost:
                            for color, cost in card.cost.items():
                                if cost > len(current_agent.cards[color]) + current_agent.gems[color]:
                                    color_needed[color] += 1
                    demand_number = sum(action['collected_gems'].get(color, 0) * color_needed[color] for color in
                                        action['collected_gems'])
                    demand_number -= sum(action['returned_gems'].get(color, 0) * color_needed[color] for color in
                                         action['returned_gems'])
                    game_features_list.append(demand_number / 68)
        else:  # If not a collect action, append zeros to the features list
            game_features_list.extend([0] * 3)

    # Find the action with the maximum Q-value
    def find_max_Qvalue_action(self, state, action):
        # Extract features from the given state and action
        action_features = self.extract_features(state, action)

        # Check if the length of features matches the length of weights
        if self.check_feature_weights(action_features):
            print("length of features and weights are not equal")
            return float('-inf')  # Return negative infinity if lengths do not match
        else:
            # Calculate the Q-value by summing the product of each feature and its corresponding weight
            return sum(action_feature * weight for action_feature, weight in zip(action_features, [
                5.562553849006237,
                11.24539817563654,
                2.952281839308075,
                51.322028650699377,
                -4.782946416215513,
                43.34450774523809
            ])) * self.alpha  # Multiply the result by the learning rate (alpha)


    # Check if the number of features matches the number of weights
    def check_feature_weights(self, action_features):
        return len(action_features) != len([5.562553849006237,
                                            11.24539817563654,
                                            2.952281839308075,
                                            51.322028650699377,
                                            -4.782946416215513,
                                            43.34450774523809])

    # Select the best action from a list of possible actions
    def SelectAction(self, actions, game_state):
        start_time, current_agent, preferred_action, max_Qvalue = time.time(), game_state.agents[
            self.id], random.choice(actions), float('-inf')
        if self.exits_actions(actions):  # Check if there are multiple actions
            for action in actions:
                if self.time_used(start_time):  # Check if the time limit is exceeded
                    break
                preferred_action = self.get_preferred_action(action, game_state, max_Qvalue, preferred_action)
        return preferred_action

    # Get the preferred action based on Q-value
    def get_preferred_action(self, action, game_state, max_Qvalue, preferred_action):
        current_Qvalue = self.find_max_Qvalue_action(game_state, action)
        if current_Qvalue > max_Qvalue:
            max_Qvalue = current_Qvalue
            preferred_action = action
        return preferred_action

    # Check if the time used exceeds a threshold
    def time_used(self, start_time):
        return time.time() - start_time > 0.9

    # Check if there are multiple actions available
    def exits_actions(self, actions):
        return len(actions) > 1
