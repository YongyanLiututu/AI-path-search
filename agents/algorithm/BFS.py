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

            score1 = -1 * cardcost1 + 1.2 * noble1 + points1

            score2 = -1 * cardcost2 + 1.2 * noble2 + points2

            return score1 > score2




    def collect_compare(self, betterActions, agent, gameState):

        score1 = 0

        lastestAction = None

        for action in betterActions:

            gemScore = {}

            for card in gameState.board.dealt[0]:

                for color in card.cost:

                    self.get_color(agent, card, color, gemScore)




            score = 0

            for color in action['collected_gems']:

                if color in gemScore:

                    score += action['collected_gems'][color] * gemScore[color]

            for color in action['returned_gems']:

                if color in gemScore:

                    score -= action['returned_gems'][color] * gemScore[color]




            if sum(card.colour in noble[1] for noble in gameState.board.nobles) > 1:

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




    def SelectAction(self, actions, gameState):

        keyCard = 3

        keyScore = 12

        agent = gameState.agents[self.id]

        lastestAction = random.choice(actions)

        if sum(len(agent.cards[key]) for key in agent.cards) < keyCard:

            return self.get_card_first(actions, agent, lastestAction, gameState)




        elif agent.score < keyScore:

            return self.nodel_first_rule(actions, agent, gameState, lastestAction)




        else:

            beginTime = time.time()

            states = set()

            queue = deque([(gameState, [])])

            while queue and time.time() - beginTime < 0.8:

                state, path = queue.popleft()

                for action in SplendorGameRule(2).getLegalActions(state, self.id):

                    nextState = deepcopy(state)

                    nextPath = path + [action]

                    goal = SplendorGameRule(2).generateSuccessor(nextState, action, self.id).agents[

                               self.id].score >= 15

                    if goal:

                        print('Path found:', nextPath)

                        return nextPath[0]

                    stateHash = hash(nextState)

                    if stateHash in states:

                        continue

                    states.add(stateHash)

                    queue.append((nextState, nextPath))




            if not path:

                return self.get_card_first(actions, agent, lastestAction, gameState)







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