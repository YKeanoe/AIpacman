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

class AlphaBetaAgent(CaptureAgent):

	# Register initial state for AlphaBetaAgent include start position of the
	# agent, closest food position to the center and timer for defensive agent,
	# and mid point for center position.
	def registerInitialState(self, gameState):
		CaptureAgent.registerInitialState(self, gameState)
		self.start = gameState.getAgentPosition(self.index)
		self.closestFoodToCenter = None
		self.timer = 0

		# Setting up center position and check if the center position has a wall.
		midHeight = gameState.data.layout.height/2
		midWidth = gameState.data.layout.width/2
		while(gameState.hasWall(midWidth, midHeight)):
			midHeight -= 1
			if midHeight == 0:
				midHeight = gameState.data.layout.height
		self.midPoint = (midWidth, midHeight)

		# Register team's agent.
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

	# Alphabeta algorithm with the usual algorithm added with visible agents.
	# If the agent are not in visible agents, it will continue the loop to the
	# next agent.
	def alphabeta(self, gameState, agent, mdepth, alpha, beta, visibleAgents):

		# restart the agent number if it passed the agents length
		if agent >= gameState.getNumAgents():
			agent = 0

		# add the depth if the alpha beta done a single loop
		if agent == self.index:
			mdepth += 1

		# pass the agent if it is not on the visible agents.
		if agent not in visibleAgents:
			return self.alphabeta(gameState, agent + 1, mdepth, alpha, beta, visibleAgents)

		# evaluate the gameState if the depth is 1 or the game is over and its the current agent.
		if mdepth == 1 or gameState.isOver():
			if agent == self.index:
				return self.evaluate(gameState)
			else:
				self.alphabeta(gameState, agent + 1, mdepth, alpha, beta, visibleAgents)

		legalActions = gameState.getLegalActions(agent)
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

	# Old expectiminimax algorithm that is not used.
	def expectiminimax(self, gameState, agent, mdepth, visibleAgents):

		if agent >= gameState.getNumAgents():
			agent = 0
			mdepth += 1

		# Depth 3 or more takes longer than 3 second
		if mdepth == 2 or gameState.isOver():
			e = self.evaluate(gameState)
			return e

		if agent not in visibleAgents:
			return self.expectiminimax(gameState, agent + 1, mdepth, visibleAgents)

		else:
			legalActions = gameState.getLegalActions(agent)
			if agent in self.agentsOnTeam:
				v = float("-inf")
				for action in legalActions:
					if action == 'Stop':
						continue
					v = max(v, self.expectiminimax(gameState.generateSuccessor(agent, action), agent + 1,mdepth, visibleAgents))
				return max(v)
			else:
				v = []
				for action in legalActions:
					expectVals = self.expectiminimax(gameState.generateSuccessor(agent, action), agent + 1,mdepth, visibleAgents)
					v.append(expectVals)
				ret = sum(v)/len(legalActions)
				return ret

	# Used to check if the current path taken will result in dead end.
	# Not finish yet so it may not work as intended.
	def iterativeDeep(self, gameState, action, visibleAgents):
		successor = gameState.generateSuccessor(self.index, action)
		depth = 0
		while depth < 5:
			legalActions = successor.getLegalActions(self.index)
			invalidActions = [action, 'Stop']
			validActions = list(set(legalActions).difference(set(invalidActions)))
			if len(validActions) == 0:
				return 0
			if len(validActions) > 1:
				return 1
			successor = gameState.generateSuccessor(self.index, action)
			depth += 1
		if set(visibleAgents).isdisjoint(self.getOpponents(gameState)):
			return 1
		else:
			return 0

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

class OffensiveAgent(AlphaBetaAgent):
	# The basic of offensive agent is to grab all the food while avoiding ghost.
	def chooseAction(self, gameState):
		start = time.time()

		# Get all visible agents
		allAgents = range(0, gameState.getNumAgents())
		visibleAgents = [a for a in allAgents if gameState.getAgentState(a).getPosition() is not None]

		# Start alpha beta pruning algorithm
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
		# Check if agent is red or blue. red team will want a higher score
		# while blue team want a lower score
		if self.red:
			features['successorScore'] = gameState.getScore()
		else:
			features['successorScore'] = -1* gameState.getScore()
		features['successorScore'] -= len(foodList)
		features['distanceToGhost'] = 0

		# Get all visible agents
		allAgents = range(0, gameState.getNumAgents())
		visibleAgents = [a for a in allAgents if gameState.getAgentState(a).getPosition() != None]

		currPos = gameState.getAgentState(self.index).getPosition()

		# Check if any opponents in visible agents.
		if not set(visibleAgents).isdisjoint(self.getOpponents(gameState)):
			# Agent will need to distance themself from ghost if agent is a pacman or agent is scared.
			if gameState.getAgentState(self.index).isPacman and gameState.getAgentState(self.index).scaredTimer > 0:
				ghosts = list(set(visibleAgents).intersection(self.getOpponents(gameState)))
				for ghost in ghosts:
					ghostPos = gameState.getAgentState(ghost).getPosition()
					dist = self.getMazeDistance(currPos, ghostPos)
					# Agent will never move to less than 2 distance.
					if dist <= 2:
						features['distanceToGhost'] = -9999
					else:
						features['distanceToGhost'] += 0.5 * dist
			# Agent does not need to further itself from the ghost but it is better to avoid/hide from it.
			else:
				ghosts = list(set(visibleAgents).intersection(self.getOpponents(gameState)))
				for ghost in ghosts:
					ghostPos = gameState.getAgentState(ghost).getPosition()
					dist = self.getMazeDistance(currPos, ghostPos)
					# print "distance to ghost ", dist
					features['distanceToGhost'] += 0.5 * dist
		# If no opponent are visible, agent will just try to read the noise distance and try to
		# stay away from it.
		else:
			ghosts = list(set(allAgents).difference(self.agentsOnTeam))
			for ghost in ghosts:
				ghostDists = gameState.getAgentDistances()
				features['distanceToGhost'] += ghostDists[ghost]

		# Agent will grab the nearest food unless it's already carrying more than 5 food.
		if gameState.getAgentState(self.index).numCarrying < 5:
			myPos = gameState.getAgentState(self.index).getPosition()
			if len(foodList) > 0:
				minDistance = min([self.getMazeDistance(myPos, food) for food in foodList])
				features['distanceToFood'] = minDistance
			else:
				myPos = gameState.getAgentState(self.index).getPosition()
				features['distanceToFood'] = self.getMazeDistance(myPos, self.start)
		else:
			myPos = gameState.getAgentState(self.index).getPosition()
			features['distanceToFood'] = self.getMazeDistance(myPos, self.start)
		return features

	def getWeights(self, gameState):
		return {'successorScore': 100, 'distanceToFood': -1, 'distanceToGhost': 1}

class DefensiveAgent(AlphaBetaAgent):
	# The basic of defensive agent is to go around the nearest food to the center to detect an enemy
	# and chase one if found.
	def chooseAction(self, gameState):
		start = time.time()

		# Get all visible agents
		allAgents = range(0, gameState.getNumAgents())
		visibleAgents = [a for a in allAgents if gameState.getAgentState(a).getPosition() is not None]

		# Start alpha beta algorithm
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

		# Minus the timer for the patrol function.
		self.timer -= 1

		return v[1]

	def getFeatures(self, gameState):
		features = util.Counter()
		myState = gameState.getAgentState(self.index)
		myPos = myState.getPosition()
		foodList = self.getFoodYouAreDefending(gameState).asList()

		# Computes distance to invaders we can see
		enemies = [gameState.getAgentState(i) for i in self.getOpponents(gameState)]
		invaders = [a for a in enemies if a.isPacman and a.getPosition() != None]
		features['numInvaders'] = len(invaders)

		# Check if any opponent is found.
		if len(invaders) > 0:
			dists = [self.getMazeDistance(myPos, a.getPosition()) for a in invaders]
			features['invaderDistance'] = max(dists)
		else:
			# If no opponent is found, patrol around the 3 nearest food to the center.
			# if the nearest food to center is set, calculate the distance.
			if self.closestFoodToCenter:
				dist = self.getMazeDistance(myPos, self.closestFoodToCenter)
			else:
				dist = None

			# Recalculate the 3 nearest food when it's already 20 actions or the food
			# is reached.
			if self.timer == 0 or dist == 0:
				self.timer = 20
				foods = []
				for food in foodList:
					foods.append((self.getMazeDistance(self.midPoint, food), food))
				foods.sort()
				chosenFood = random.choice(foods[:3])
				self.closestFoodToCenter = chosenFood[1]
			dist = self.getMazeDistance(myPos, self.closestFoodToCenter)
			features['invaderDistance'] = dist
		return features

	def getWeights(self, gameState):
		return {'numInvaders': -1000, 'invaderDistance': -10, 'stop': -100, 'reverse': -2}