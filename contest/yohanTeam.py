# myTeam.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from captureAgents import CaptureAgent
import random, time, util
from game import Directions
import game

#################
# Team creation #
#################

def createTeam(firstIndex, secondIndex, isRed,
               first = 'OffensiveAgent', second = 'DefensiveAgent'):
	return [eval(first)(firstIndex), eval(second)(secondIndex)]

##########
# Agents #
##########

class ExpectimaxAgent(CaptureAgent):

	def registerInitialState(self, gameState):
		CaptureAgent.registerInitialState(self, gameState)
		self.start = gameState.getAgentPosition(self.index)

		agentsTeam = []
		agentsLen = gameState.getNumAgents()
		i = self.index
		while len(agentsTeam) < (agentsLen/2):
			agentsTeam.append(i)
			i += 2
			if i >= agentsLen:
				i = 0
		agentsTeam.sort()
		self.registerTeam(agentsTeam)

	def baseSearch(self, gameState):
		"""
        Picks among the actions with the highest Q(s,a).
        """
		actions = gameState.getLegalActions(self.index)

		# You can profile your evaluation time by uncommenting these lines
		# start = time.time()
		v = []
		for action in actions:
			if action == 'Stop':
				continue
			successor = gameState.generateSuccessor(self.index, action)
			v.append((self.evaluate(successor), action))

		# print 'eval time for agent %d: %.4f' % (self.index, time.time() - start)

		print "Values in baseSearch ", v
		maxValues = [i for i in v if i == max(v)]
		maxValue = random.choice(maxValues)

		# print maxValue
		bestAction = maxValue[1]
		# print bestAction
		foodLeft = len(self.getFood(gameState).asList())
		# print foodLeft
		if foodLeft <= 2:
			# print "foodl <= 2"
			bestDist = 9999
			for action in actions:
				if action == 'Stop':
					continue
				successor = gameState.generateSuccessor(self.index, action)
				pos2 = successor.getAgentPosition(self.index)
				dist = self.getMazeDistance(gameState.getAgentPosition(self.index), pos2)
				# print "Comparing {0} < {1}".format(dist, bestDist)
				if dist < bestDist:
					# print "Change action to ",action
					bestAction = action
					bestDist = dist
			print "Base search return with ", bestAction
			return bestAction
		print "Base search return with ",bestAction
		return bestAction


	def expectiminimax(self, gameState, agent, mdepth, visibleAgents):
		# print "start expectimax with agent {0} at depth {1}".format(agent, mdepth)

		if agent >= gameState.getNumAgents():
			# print "agent rollback to 0"
			agent = 0
			mdepth += 1
			# print "continue expectimax with agent {0} at depth {1}".format(agent, mdepth)



		if mdepth == 1 or gameState.isOver():
			# print "stopping"
			e = self.evaluate(gameState)
			# print "evaluate = ",e
			return e

		if agent not in visibleAgents:
			# print "agent {0} not visible".format(agent)
			return self.expectiminimax(gameState, agent + 1, mdepth, visibleAgents)

		else:
			# print "Getting legalActions for agent {0}".format(agent)
			legalActions = gameState.getLegalActions(agent)
			if agent in self.agentsOnTeam:
				# v = float("-inf")
				v = []
				for action in legalActions:
					if action == 'Stop':
						continue
					v.append(self.expectiminimax(gameState.generateSuccessor(agent, action), agent + 1,mdepth, visibleAgents))
					# v = max(v, self.expectiminimax(gameState.generateSuccessor(agent, action), agent + 1,mdepth, visibleAgents))
				# print v
				return max(v)
			else:
				v = []
				for action in legalActions:
					expectVals = self.expectiminimax(gameState.generateSuccessor(agent, action), agent + 1,mdepth, visibleAgents)
					v.append(expectVals)
				ret = sum(v)/len(legalActions)
				# print ret
				return ret

	def getFeatures(self, gameState):
		"""
		Returns a counter of features for the state
		"""
		features = util.Counter()
		features['successorScore'] = self.getScore(gameState)
		return features


	def getWeights(self, gameState):
		"""
		Normally, weights do not depend on the gamestate.  They can be either
		a counter or a dictionary.
		"""
		return {'successorScore': 1.0}


	def evaluate(self, gameState):
		"""
		Computes a linear combination of features and feature weights
		"""
		features = self.getFeatures(gameState)
		weights = self.getWeights(gameState)
		return features * weights

class OffensiveAgent(ExpectimaxAgent):

	def chooseAction(self, gameState):

		# Get all visible agents
		allAgents = range(0, gameState.getNumAgents() - 1)
		visibleAgents = [a for a in allAgents if gameState.getAgentState(a).getPosition() is not None]
		print visibleAgents

		print gameState.getAgentState(1).getPosition()
		print gameState.getAgentState(3).getPosition()
		# print gameState.getAgentState(self.index).isPacman

		ourAgent = self.getOpponents(gameState)
		# print ourAgent



		# if not set(visibleAgents).isdisjoint(self.getOpponents(gameState)):
		print "Starting expetiminimax"
		v = []
		agent = self.index
		legalActions = gameState.getLegalActions(self.index)
		for action in legalActions:
			# print "{0} for agent".format(agent)
			if action == 'Stop':
				continue
			expectVals = self.expectiminimax(gameState.generateSuccessor(agent,action), agent+1, 0, visibleAgents)
			v.append((expectVals, action))
		print "Expectiminimax val = ", v
		vBestScore = max(v)
		bestIndices = [index for index in range(len(v)) if v[index] == vBestScore]
		chosenIndex = random.choice(bestIndices) # Pick randomly among the best
		print "Expectiminimax return with ", v[chosenIndex][1]
		return v[chosenIndex][1]
		# return random.choice(legalActions)
		# else:
		# 	return self.baseSearch(gameState)

	def getFeatures(self, gameState):
		features = util.Counter()
		foodList = self.getFood(gameState).asList()
		features['successorScore'] = -len(foodList)  # self.getScore(successor)

		# 	# Get all visible agents
		allAgents = range(0, gameState.getNumAgents() - 1)
		visibleAgents = [a for a in allAgents if gameState.getAgentState(a).getPosition() != None]

		score = gameState.getScore()
		currPos = gameState.getAgentState(self.index).getPosition()

		if not set(visibleAgents).isdisjoint(self.getOpponents(gameState)):
			ghosts = list(set(visibleAgents).intersection(self.getOpponents(gameState)))
			# print ghosts
			for ghost in ghosts:
				if gameState.getAgentState(ghost).isPacman:
					continue
				ghostPos = gameState.getAgentState(ghost).getPosition()
				dist = self.getMazeDistance(currPos, ghostPos)
				# print "distance to ghost ", dist
				if dist <= 2:
					features['successorScore'] = -9999
				else:
					features['successorScore'] += 2 * dist

		# Compute distance to the nearest food

		if len(foodList) > 0:  # This should always be True,  but better safe than sorry
			myPos = gameState.getAgentState(self.index).getPosition()
			minDistance = min([self.getMazeDistance(myPos, food) for food in foodList])
			features['distanceToFood'] = minDistance
		return features

	def getWeights(self, gameState):
		return {'successorScore': 100, 'distanceToFood': -1}

	# def evaluate(self, gameState):
	# 	"""
     #    Computes a linear combination of features and feature weights
     #    """
	# 	features = self.getFeatures(gameState)
	# 	print features
	# 	weights = self.getWeights(gameState)
	# 	print weights
	# 	print features * weights
	# 	print type(features)
	# 	print type(weights)
	# 	return features * weights

	def evaluate(self, gameState):
		"""
		Score = 1 * currentScore
				- 1 * distance to closest food
				- 2 * distance to closest non scared ghost
				- 20 * distance to closest capsule
		"""
		# print "eva"


		# Get all visible agents
		allAgents = range(0, gameState.getNumAgents() - 1)
		visibleAgents = [a for a in allAgents if gameState.getAgentState(a).getPosition() != None]

		score = gameState.getScore()
		currPos = gameState.getAgentState(self.index).getPosition()

		# print "CurrPos {0}, self.start {1}".format(currPos, self.start)
		# if currPos == self.start:
		# 	print "Dying"
		# 	return float('-inf')

		if not set(visibleAgents).isdisjoint(self.getOpponents(gameState)):
			ghosts = list(set(visibleAgents).intersection(self.getOpponents(gameState)))
			# print ghosts
			for ghostIndex in ghosts:
				ghost = gameState.getAgentState(ghostIndex)
				if ghost.isPacman:
					continue
				ghostPos = ghost.getPosition()
				if ghost.scaredTimer == 0:
					dist = self.getMazeDistance(currPos, ghostPos)
					# print "distance to ghost ", dist
					if dist <= 2:
						return float('-inf')


		capsules = self.getCapsules(gameState)
		foodList = self.getFood(gameState).asList()

		# Return home when half of the food is eaten
		# if gameState.getAgentState(self.index).numCarrying >= len(foodList):
		# 	score -= 1000 * self.getMazeDistance(currPos, self.start)
		# else:
		score -= 100 * len(foodList)
		# score -= 100 * len(capsules)

		score -= min([self.getMazeDistance(currPos, food) for food in foodList])
			# score -= min([self.getMazeDistance(currPos, capsule) for capsule in capsules])

			# score += 2 * gameState.getAgentState(self.index).numCarrying


			# for food in foodList:
			# 	score -= 1.5 * self.getMazeDistance(currPos, food)
			#
			#
			# for capsule in capsules:
			# 	score -= 2 * self.getMazeDistance(currPos, capsule)

			# print "eva return with score ", score
		return score


class DefensiveAgent(ExpectimaxAgent):
	def chooseAction(self, gameState):
		legalActions = gameState.getLegalActions(self.index)
		return random.choice(legalActions)
		# return self.baseSearch(gameState)

	def getFeatures(self, gameState):
		features = util.Counter()

		myState = gameState.getAgentState(self.index)
		myPos = myState.getPosition()

		# Computes whether we're on defense (1) or offense (0)
		features['onDefense'] = 1
		if myState.isPacman: features['onDefense'] = 0

		# Computes distance to invaders we can see
		enemies = [gameState.getAgentState(i) for i in self.getOpponents(gameState)]
		invaders = [a for a in enemies if a.isPacman and a.getPosition() != None]
		features['numInvaders'] = len(invaders)
		if len(invaders) > 0:
			dists = [self.getMazeDistance(myPos, a.getPosition()) for a in invaders]
			features['invaderDistance'] = min(dists)

		return features








