from template import Agent
import random, time
from copy import deepcopy
from collections import deque
from Splendor.splendor_model import SplendorGameRule


class myAgent(Agent):
    def __init__(self, _id):
        super().__init__(_id)

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
            score1 = -1 * cardcost1 + 1.7 * noble1 + points1
            score2 = -1 * cardcost2 + 1.7 * noble2 + points2

            return score1 > score2

    def collect_compare(self, betterActions, agent, game_state):
        score1 = 0
        lastestAction = None
        for action in betterActions:
            gemScore = {}

            for card in game_state.board.dealt[0]:
                if card is not None and card.cost is not None:
                    for color in card.cost:
                        self.get_color(agent, card, color, gemScore)

            score = sum(action['collected_gems'].get(color, 0) * gemScore.get(color, 0) for color in
                        action['collected_gems']) - sum(
                action['returned_gems'].get(color, 0) * gemScore.get(color, 0) for color in action['returned_gems'])
            if sum(card.colour in noble[1] for noble in game_state.board.nobles) > 1:
                score += 1

            if score > score1:
                score1 = score
                lastestAction = action

        return lastestAction

    def get_color(self, agent, card, color, colorScore):
        if card.cost[color] > len(agent.cards[color]) + agent.gems[color]:
            if color not in colorScore:
                colorScore[color] = 0
            colorScore[color] += 1

    def heuristic(self, state):
        return sum(
            card.points - sum(abs(state.agents[self.id].gems[colour] - number) for colour, number in card.cost.items())
            for card in state.board.dealt_list()
        )

    def SelectAction(self, actions, game_state):
        keyCard = 3
        keyScore = 12
        beginTime = time.time()
        states = set()
        stack = [(game_state, [])]
        agent = game_state.agents[self.id]
        lastestAction = random.choice(actions)
        if sum(len(agent.cards[key]) for key in agent.cards) < keyCard:
            return self.get_card_first(actions, agent, lastestAction, game_state)

        elif agent.score < keyScore:
            return self.nodel_first_rule(actions, agent, game_state, lastestAction)

        else:
            depth_limit = 1
            while time.time() - beginTime < 0.8:
                result = self.iterative_deepening_search(game_state, actions, depth_limit, beginTime)
                if result:
                    return result
                depth_limit += 1

            return self.nodel_first_rule(actions, agent, game_state, lastestAction)

    def nodel_first_rule(self, actions, agent, game_state, lastestAction):
        for action in actions:
            if 'buy' in action['type']:
                lastestAction = action
                for action in actions:
                    if 'buy' in action['type'] and self.action_compare(2, game_state, action, lastestAction):
                        lastestAction = action
                return lastestAction
        else:
            reserveScores = []
            for action in actions:
                if 'reserve' in action['type'] and action['card'].deck_id == 3:
                    card = action['card']
                    gemsDifference = sum(max(card.cost[color] - len(agent.cards[color]) - agent.gems[color], 0) for color in card.cost)
                    noblesInterest = sum(card.colour in noble[1] for noble in game_state.board.nobles)
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
                return lastestAction if not betterActions else self.collect_compare(betterActions, agent, game_state)

    def iterative_deepening_search(self, game_state, actions, depth_limit, beginTime):
        stack = [(game_state, [], 0)]
        states = set()

        while stack and time.time() - beginTime < 0.5:
            state, path, depth = stack.pop()

            if depth >= depth_limit:
                continue

            for action in SplendorGameRule(2).getLegalActions(state, self.id):
                next_state = deepcopy(state)
                next_path = path + [action]
                goal = SplendorGameRule(2).generateSuccessor(next_state, action, self.id).agents[self.id].score >= 15
                if goal:
                    print('Path found:', next_path)
                    return next_path[0]

                state_hash = hash(next_state)
                if state_hash in states:
                    continue
                states.add(state_hash)
                stack.append((next_state, next_path, depth + 1))

            stack.sort(key=lambda item: self.heuristic(item[0]))

        return None

    def get_card_first(self, actions, agent, keyAction, game_state):
        for action in actions:
            if 'buy' in action['type']:
                keyAction = action
                for action in actions:
                    if 'buy' in action['type'] and self.action_compare(1, game_state, action, keyAction):
                        keyAction = action
                return keyAction
        else:
            return keyAction if not (betterActions := [x for x in actions if 'collect' in x['type']]) else self.collect_compare(betterActions, agent, game_state)