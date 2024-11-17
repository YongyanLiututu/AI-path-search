from template import Agent

import random, time

from copy import deepcopy
import copy
from collections import deque

from Splendor.splendor_model import SplendorGameRule




class myAgent(Agent):

    def __init__(self, _id):

        super().__init__(_id)
        self.visited_states = set()




    def action_compare(self, turn, state, action1, action2):

        if turn == 1:

            cardcost1 = sum(action1['card'].cost.values())

            cardcost2 = sum(action2['card'].cost.values())

            noble1 = sum(action1['card'].colour in noble[1] for noble in state.board.nobles)

            noble2 = sum(action2['card'].colour in noble[1] for noble in state.board.nobles)

            points1 = action1['card'].points

            points2 = action2['card'].points

            score1 = -1 * cardcost1 + 0.7 * noble1 + points1

            score2 = -1 * cardcost2 + 0.7 * noble2 + points2

            return score1 > score2







        else:




            if sum(action1['card'].colour in noble[1] for noble in state.board.nobles) != sum(

                    action2['card'].colour in noble[1] for noble in state.board.nobles):

                return sum(action1['card'].colour in noble[1] for noble in state.board.nobles) > sum(

                    action2['card'].colour in noble[1] for noble in state.board.nobles)




            if action1['card'].points != action2['card'].points:

                return action1['card'].points > action2['card'].points




            if sum(action1['card'].cost.values()) != sum(action2['card'].cost.values()):

                return sum(action1['card'].cost.values()) < sum(action2['card'].cost.values())

            cardcost1 = sum(action1['card'].cost.values())

            cardcost2 = sum(action2['card'].cost.values())

            noble1 = sum(action1['card'].colour in noble[1] for noble in state.board.nobles)

            noble2 = sum(action2['card'].colour in noble[1] for noble in state.board.nobles)

            points1 = action1['card'].points

            points2 = action2['card'].points

            score1 = -1 * cardcost1 + 1.2 * noble1 + points1

            score2 = -1 * cardcost2 + 1.2 * noble2 + points2

            return score1 > score2

    def remove_card_from_reserved(self, board_state, deck_id, card):
      
        if hasattr(board_state, 'reserved') and deck_id in board_state.reserved:
       
            if card in board_state.reserved[deck_id]:
                board_state.reserved[deck_id].remove(card)
            else:
                print("Card not found in the reserved list for deck", deck_id)
        else:
            print("Reserved list does not exist or deck_id", deck_id, "not found in reserved list")

    def get_color(self, agent, card, color, colorScore):

        if card.cost[color] > len(agent.cards[color]) + agent.gems[color]:

            if color not in colorScore:

                colorScore[color] = 0

            colorScore[color] += 1

    def heuristic(self, state):
        agent = state.agents[self.id]
        opponent_id = 1 - self.id
        opponent = state.agents[opponent_id]
        score = agent.score
        gem_score = sum(agent.gems.values()) - sum(opponent.gems.values())
        deck_score = sum(len(agent.cards[key]) for key in agent.cards)
        opponent_score = opponent.score
        final_score = score + 0.5 * gem_score + 0.3 * deck_score - 0.2 * opponent_score

        return final_score



    def SelectAction(self, actions, gameState):

        keyCard = 3

        keyScore = 6

        agent = gameState.agents[self.id]

        lastestAction = random.choice(actions)

        if sum(len(agent.cards[key]) for key in agent.cards) < keyCard:

            return self.get_card_first(actions, agent, lastestAction, gameState)




        elif agent.score < keyScore:

            return self.nodel_first_rule(actions, agent, gameState, lastestAction)




        else:

            beginTime = time.time()
            best_action = self.get_card_first(actions, agent, lastestAction, gameState)
            best_eval = float('-inf')
            max_depth = 1
            max_loops = 3
            loops = 0

            while loops < max_loops and time.time() - beginTime < 0.7:
                for action in actions:
                    next_state =copy.copy(gameState)

                    eval = self.heuristic(next_state) if max_depth == 1 else self.minimax(next_state,
                                                                                          depth=max_depth - 1,
                                                                                          alpha=float('-inf'),
                                                                                          beta=float('inf'),
                                                                                          maximizing_player=False)

                    if eval > best_eval:
                        best_eval = eval
                        best_action = action
                if best_action is not None:
                    break
                max_depth += 1
                loops += 1
            return best_action

    def is_terminal_state(self, state):
        return any(agent.score >= 15 for agent in state.agents)

    def collect_compare(self, betterActions, agent, game_state):
        score1 = 0
        lastestAction = None
        for action in betterActions:
            gemScore = {}

            for card in game_state.board.dealt[0]:
                if card is not None:
                    if card.cost is not None:
                        for color in card.cost:
                            self.get_color(agent, card, color, gemScore)
                    else:
                        print("card.cost is None:", card)
                else:
                    print("card is None in game_state.board.dealt[0]")

            score = sum(action['collected_gems'].get(color, 0) * gemScore.get(color, 0) for color in
                        action['collected_gems']) - sum(
                action['returned_gems'].get(color, 0) * gemScore.get(color, 0) for color in action['returned_gems'])
            if sum(card.colour in noble[1] for noble in game_state.board.nobles) > 1:
                score += 1

            if score > score1:
                score1 = score
                lastestAction = action

        return lastestAction


    def nodel_first_rule(self, actions, agent, gameState, lastestAction):

        for action in actions:

            if 'buy' in action['type']:

                lastestAction = action

                for action in actions:

                    if 'buy' in action['type'] and self.action_compare(2, gameState, action, lastestAction):

                        lastestAction = action

                return lastestAction

        else:

            reserveScores = []

            for action in actions:

                if 'reserve' in action['type'] and action['card'].deck_id == 3:

                    card = action['card']

                    gemsDifference = sum(

                        max(card.cost[color] - len(agent.cards[color]) - agent.gems[color], 0) for color in

                        card.cost)

                    noblesInterest = sum(card.colour in noble[1] for noble in gameState.board.nobles)

                    if noblesInterest >= 2:

                        noblesInterest *= 0.7

                    score = action['card'].points / (gemsDifference + 1) + 0.5 * noblesInterest

                    reserveScores.append((score, action))




            if reserveScores:

                reserveScores.sort(reverse=True)

                lastestAction = reserveScores[0][1]

                return lastestAction

            else:

                betterActions = [action for action in actions if 'collect' in action['type']]

                if len(betterActions) == 0:

                    return lastestAction

                else:

                    lastestAction = self.collect_compare(betterActions, agent, gameState)

                    return lastestAction




    def get_card_first(self, actions, agent, keyAction, gameState):

        for action in actions:

            if 'buy' in action['type']:

                keyAction = action

                for action in actions:

                    if 'buy' in action['type'] and self.action_compare(1, gameState, action, keyAction):

                        keyAction = action

                return keyAction

        else:

            betterActions = [x for x in actions if 'collect' in x['type']]

            if len(betterActions) == 0:

                return keyAction

            else:

                keyAction = self.collect_compare(betterActions, agent, gameState)

                return keyAction





    def minimax(self, state, depth, alpha, beta, maximizing_player):

        if state in self.visited_states:
            return self.heuristic(state)


        if depth == 0 or self.is_terminal_state(state):
            return self.heuristic(state)

        if maximizing_player:
            max_eval = float('-inf')
            for action in SplendorGameRule(2).getLegalActions(state, self.id):

                next_state = self.simulate_action(action, state, self.id)
                eval = self.heuristic(next_state) if depth == 1 else self.minimax(next_state, depth - 1, alpha, beta,
                                                                                  False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            opponent_id = 1 - self.id
            for action in SplendorGameRule(2).getLegalActions(state, opponent_id):

                next_state = deepcopy(state)
                SplendorGameRule(2).generateSuccessor(next_state, action, opponent_id)
                eval = self.heuristic(next_state) if depth == 1 else self.minimax(next_state, depth - 1, alpha, beta,
                                                                                  True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval



    def simulate_action(self, action, state, agent_id):
        agent = state.agents[agent_id]
        next_state = state

        if 'card' in action:
            card = action['card']


            for row_idx, row in enumerate(next_state.board.dealt):
                for col_idx, dealt_card in enumerate(row):
                    try:
                        # If the dealt card matches the target card
                        if dealt_card == card:
                            # Perform action if the card is found
                            # Decrement gem stacks by returned_gems
                            for colour, count in action['returned_gems'].items():
                                agent.gems[colour] -= count
                                next_state.board.gems[colour] += count

                            if 'buy' in action['type']:
                                # If buying one of the available cards on the board, set removed card slot to new dealt card.
                                next_state.board.dealt[row_idx][col_idx] = next_state.board.deal(card.deck_id)

                                # Else, agent is buying a reserved card. Remove card from player's yellow stack.
                                if card in agent.cards['yellow']:
                                    agent.cards['yellow'].remove(card)

                                # Add card to player's stack of matching colour, and increment agent's score accordingly.
                                agent.cards[card.colour].append(card)
                                agent.score += card.points
                            elif action['type'] == 'reserve':
                                # Remove card from dealt cards by locating via unique code.
                                next_state.board.dealt[row_idx][col_idx] = next_state.board.deal(card.deck_id)

                                # Add card to player's yellow stack.
                                agent.cards['yellow'].append(card)

                            # Exit the loop once the card is found and action is performed
                            return next_state
                    except AttributeError:
                        pass

        return next_state







