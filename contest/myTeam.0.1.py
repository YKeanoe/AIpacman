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

		self.furthestFood = None
		self.timer = 0

		midHeight = gameState.data.layout.height/2
		midWidth = gameState.data.layout.width/2
		while(gameState.hasWall(midWidth, midHeight)):
			midHeight -= 1

		self.midPoint = ( midWidth, midHeight )


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

		# print "Values in baseSearch ", v
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
			# print "Base search return with ", bestAction
			return bestAction
		# print "Base search return with ",bestAction
		return bestAction


	def alphabeta(self, gameState, agent, mdepth, alpha, beta, visibleAgents):

		if agent >= gameState.getNumAgents():
			agent = 0
		if agent == self.index:
			mdepth += 1

		if agent not in visibleAgents:
			return self.alphabeta(gameState, agent + 1, mdepth, alpha, beta, visibleAgents)

		legalActions = gameState.getLegalActions(agent)

		if (mdepth == 1 or gameState.isOver()) and agent == self.index:
			return self.evaluate(gameState)
		else:
			self.alphabeta(gameState, agent + 1, mdepth, alpha, beta, visibleAgents)

		# tempActions = list(set(legalActions).difference(['Stop']))

		if agent in self.agentsOnTeam:
			v = float("-inf")
			for action in legalActions:
				v = max(v, self.alphabeta(gameState.generateSuccessor(agent, action), agent + 1,mdepth, alpha, beta, visibleAgents))
				if v > beta:
					return v
				alpha = max(alpha, v)
			return v
		else:
			v = float("inf")
			for action in legalActions:
				v = min(v, self.alphabeta(gameState.generateSuccessor(agent, action), agent + 1,mdepth, alpha, beta, visibleAgents))
				if v < alpha:
					return v
				beta = min(beta, v)
			return v

	def expectiminimax(self, gameState, agent, mdepth, visibleAgents):
		# print "start expectimax with agent {0} at depth {1}".format(agent, mdepth)

		if agent >= gameState.getNumAgents():
			# print "agent rollback to 0"
			agent = 0
			mdepth += 1
			# print "continue expectimax with agent {0} at depth {1}".format(agent, mdepth)


		# Depth 3 or more takes longer than 3 second
		if mdepth == 2 or gameState.isOver():
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
		start = time.time()

		# Get all visible agents
		allAgents = range(0, gameState.getNumAgents())
		visibleAgents = [a for a in allAgents if gameState.getAgentState(a).getPosition() is not None]

		v = (float("-inf"), 'None')
		alpha = float('-inf')
		beta = float('inf')
		legalActions = gameState.getLegalActions(self.index)
		for action in legalActions:
			if action == 'Stop':
				continue
			v = max(v, (self.alphabeta(gameState.generateSuccessor(self.index, action), self.index+1, 0, alpha, beta, visibleAgents), action))
			if v[0] > beta:
				print "Agent {0} chose {1} with value {2}".format(self.index, v[1], v[0])
				print 'Execution time for agent %d: %.4f' % (self.index, time.time() - start)
				return v[1]
			alpha = max(alpha, v[0])
		print "Agent {0} chose {1} with value {2}".format(self.index, v[1], v[0])
		print 'Execution time for agent %d: %.4f' % (self.index, time.time() - start)
		return v[1]

	def getFeatures(self, gameState):
		features = util.Counter()
		foodList = self.getFood(gameState).asList()
		if self.red:
			features['successorScore'] = gameState.getScore()  # self.getScore(successor)
		else:
			features['successorScore'] = -1* gameState.getScore()  # self.getScore(successor)
		features['successorScore'] -= len(foodList)  # self.getScore(successor)
		features['distanceToGhost'] = 0

		# 	# Get all visible agents
		allAgents = range(0, gameState.getNumAgents())
		visibleAgents = [a for a in allAgents if gameState.getAgentState(a).getPosition() != None]

		currPos = gameState.getAgentState(self.index).getPosition()


		if not set(visibleAgents).isdisjoint(self.getOpponents(gameState)):
			# print "ghost visible"
			if gameState.getAgentState(self.index).isPacman and gameState.getAgentState(self.index).scaredTimer > 0:
				# print "ghost visible, we pacman, and ghost aint scared"
				ghosts = list(set(visibleAgents).intersection(self.getOpponents(gameState)))
				for ghost in ghosts:
					ghostPos = gameState.getAgentState(ghost).getPosition()
					dist = self.getMazeDistance(currPos, ghostPos)
					# print "distance to ghost ", dist
					if dist <= 2:
						features['distanceToGhost'] = -9999
					else:
						features['distanceToGhost'] += 0.5 * dist
			else:
			# 	print "ghost visible but we aint pacman or ghosts scared"
				ghosts = list(set(visibleAgents).intersection(self.getOpponents(gameState)))
				for ghost in ghosts:
					ghostPos = gameState.getAgentState(ghost).getPosition()
					dist = self.getMazeDistance(currPos, ghostPos)
					# print "distance to ghost ", dist
					features['distanceToGhost'] += 0.5 * dist
		else:
			# print "ghost aint visible"
			ghosts = list(set(allAgents).difference(self.agentsOnTeam))
			for ghost in ghosts:
				ghostDists = gameState.getAgentDistances()
				# print "distance to ghost ", ghostDists[ghost]
				features['distanceToGhost'] += ghostDists[ghost]

		# Compute distance to the nearest food
		# myPos = gameState.getAgentState(self.index).getPosition()
		# print self.getMazeDistance(myPos, self.start)
		if gameState.getAgentState(self.index).numCarrying < 5:  # This should always be True,  but better safe than sorry
			myPos = gameState.getAgentState(self.index).getPosition()
			if len(foodList) > 0:
				minDistance = min([self.getMazeDistance(myPos, food) for food in foodList])
				features['distanceToFood'] = minDistance
			else:
				myPos = gameState.getAgentState(self.index).getPosition()
				features['distanceToFood'] = self.getMazeDistance(myPos, self.start)
		else:
			# print "bring food home"
			myPos = gameState.getAgentState(self.index).getPosition()
			features['distanceToFood'] = self.getMazeDistance(myPos, self.start)
			# print features
		return features

	def getWeights(self, gameState):
		return {'successorScore': 100, 'distanceToFood': -1, 'distanceToGhost': 1}

class DefensiveAgent(ExpectimaxAgent):
	def chooseAction(self, gameState):
		start = time.time()


		# Get all visible agents
		allAgents = range(0, gameState.getNumAgents())
		visibleAgents = [a for a in allAgents if gameState.getAgentState(a).getPosition() is not None]

		v = (float("-inf"), 'None')
		alpha = float('-inf')
		beta = float('inf')
		legalActions = gameState.getLegalActions(self.index)
		for action in legalActions:
			if action == 'Stop':
				continue
			v = max(v, (self.alphabeta(gameState.generateSuccessor(self.index, action), self.index+1, 0, alpha, beta, visibleAgents), action))
			if v[0] > beta:
				print "Agent {0} chose {1} with value {2}".format(self.index, v[1], v[0])
				print 'Execution time for agent %d: %.4f' % (self.index, time.time() - start)
				return v[1]
			alpha = max(alpha, v[0])
		print "Agent {0} chose {1} with value {2}".format(self.index, v[1], v[0])
		print 'Execution time for agent %d: %.4f' % (self.index, time.time() - start)
		self.timer -= 1
		print self.furthestFood
		return v[1]


	def getFeatures(self, gameState):
		features = util.Counter()

		myState = gameState.getAgentState(self.index)
		myPos = myState.getPosition()

		# Computes whether we're on defense (1) or offense (0)
		# features['onDefense'] = 1
		# if myState.isPacman: features['onDefense'] = 0

		# Computes distance to invaders we can see
		enemies = [gameState.getAgentState(i) for i in self.getOpponents(gameState)]
		invaders = [a for a in enemies if a.isPacman and a.getPosition() != None]
		features['numInvaders'] = len(invaders)

		foodList = self.getFoodYouAreDefending(gameState).asList()

		if len(invaders) > 0:
			dists = [self.getMazeDistance(myPos, a.getPosition()) for a in invaders]
			features['invaderDistance'] = max(dists)
		else:

			if self.furthestFood:
				dist = self.getMazeDistance(myPos, self.furthestFood)
			else:
				dist = None

			if self.timer == 0 or dist == 0:
				self.timer = 20

				foods = []
				for food in foodList:
					foods.append((self.getMazeDistance(self.midPoint, food), food))
				foods.sort()
				print foods
				print foods[:3]
				chosenFood = random.choice(foods[:3])
				# print chosenFood
				self.furthestFood = chosenFood[1]

			dist = self.getMazeDistance(myPos, self.furthestFood)

			features['invaderDistance'] = dist

			# dists = [self.getMazeDistance(myPos, a) for a in foodList]
			# features['invaderDistance'] = random.choice(dists)

		return features

	def getWeights(self, gameState):
		return {'numInvaders': -1000, 'onDefense': 100, 'invaderDistance': -10, 'stop': -100, 'reverse': -2}