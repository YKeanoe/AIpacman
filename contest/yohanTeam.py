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
			successor = gameState.generateSuccessor(self.index, action)
			v.append((self.evaluate(successor), action))

		# print 'eval time for agent %d: %.4f' % (self.index, time.time() - start)
		print "aaaaaaaaaaaaaaaaaaaaaaaaaaaa"
		print

		print v
		maxValue = max(v)
		print maxValue
		bestAction = maxValue[1]
		print bestAction
		foodLeft = len(self.getFood(gameState).asList())
		print foodLeft
		if foodLeft <= 2:
			print "foodl <= 2"
			bestDist = 9999
			for action in actions:
				successor = gameState.generateSuccessor(self.index, action)
				pos2 = successor.getAgentPosition(self.index)
				dist = self.getMazeDistance(gameState.getAgentPosition(self.index), pos2)
				if dist < bestDist:
					bestAction = action
					bestDist = dist
			print bestAction
			return bestAction
		print bestAction
		return bestAction


	def expectiminimax(self, gameState, agent, mdepth, visibleAgents):
		print "start expectimax with agent {0} at depth {1}".format(agent, mdepth)

		if agent >= gameState.getNumAgents():
			print "agent rollback to 0"
			agent = 0
			mdepth += 1
			print "continue expectimax with agent {0} at depth {1}".format(agent, mdepth)



		if mdepth == 5 or gameState.isOver():
			print "stopping"
			return self.evaluate(gameState)

		if agent not in visibleAgents:
			print "agent {0} not visible".format(agent)
			self.expectiminimax(gameState, agent + 1, mdepth, visibleAgents)
		else:
			print "Getting legalActions for agent {0}".format(agent)
			legalActions = gameState.getLegalActions(agent)
			if agent in self.agentsOnTeam:
				v = float("-inf")
				for action in legalActions:
					if action == 'Stop':
						continue
					v = max(v, self.expectiminimax(gameState.generateSuccessor(agent, action), agent + 1,mdepth, visibleAgents))
				return v
			else:
				v = []
				for action in legalActions:
					expectVals = self.expectiminimax(gameState.generateSuccessor(agent, action), agent + 1,mdepth, visibleAgents)
					v.append(expectVals)
				ret = sum(v)/len(legalActions)
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
		print "evaluating"
		features = self.getFeatures(gameState)
		weights = self.getWeights(gameState)
		print "evaluate complete with value {0}".format(features * weights)
		return features * weights

class OffensiveAgent(ExpectimaxAgent):

	def chooseAction(self, gameState):

		# Get all visible agents
		allAgents = range(0, gameState.getNumAgents() - 1)
		visibleAgents = [a for a in allAgents if gameState.getAgentState(a).getPosition() != None]
		print visibleAgents

		ourAgent = self.getOpponents(gameState)
		print ourAgent

		if set(visibleAgents) in self.getOpponents(gameState):
			v = []
			agent = self.index
			legalActions = gameState.getLegalActions(self.index)
			for action in legalActions:
				print "{0} for agent".format(agent)
				if action == 'Stop':
					continue
				expectVals = self.expectiminimax(gameState.generateSuccessor(agent,action), agent+1, 0, visibleAgents)
				v.append((expectVals, action))
			vBestScore = max(v)
			bestIndices = [index for index in range(len(v)) if v[index] == vBestScore]
			chosenIndex = random.choice(bestIndices) # Pick randomly among the best
			return v[chosenIndex][1]
			# return random.choice(legalActions)
		else:
			return self.baseSearch(gameState)

	def getFeatures(self, gameState):
		features = util.Counter()
		foodList = self.getFood(gameState).asList()
		features['successorScore'] = -len(foodList)  # self.getScore(successor)

		# Compute distance to the nearest food

		if len(foodList) > 0:  # This should always be True,  but better safe than sorry
			myPos = gameState.getAgentState(self.index).getPosition()
			minDistance = min([self.getMazeDistance(myPos, food) for food in foodList])
			features['distanceToFood'] = minDistance
		return features

	def getWeights(self, gameState):
		return {'successorScore': 100, 'distanceToFood': -1}

	"""
	def evaluate(self, currentGameState):

		Score = 1 * currentScore
				- 1 * distance to closest food
				- 2 * distance to closest non scared ghost
				- 20 * distance to closest capsule

		print "eva"
		newGhostStates = currentGameState.getGhostStates()
		newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
		newCapsules = currentGameState.getCapsules()
	
		foodDistance = []
		ghostDistance = []
		foodList = currentGameState.getFood().asList()
		currPos = currentGameState.getAgentState(self.index).getPosition()

		score = currentGameState.getScore()


		score -= len(foodList)
		score -= len(newCapsules)
		for ghostState in newGhostStates:
			dist = manhattanDistance(ghostState.getPosition(),pacmanPos)
			if ghostState.scaredTimer > 0:
				if ghostState.scaredTimer > dist:
					score += 2 * dist
				else:
					score += 1.5 * dist
			else:
				score -= 1.5 * dist
		
		for food in foodList:
			score -= 0.5 * self.getMazeDistance(myPos, food)
	
		
		for capsule in newCapsules:
			score -= 2 * manhattanDistance(capsule,pacmanPos)

		return score
	"""

class DefensiveAgent(ExpectimaxAgent):
	def chooseAction(self, gameState):
		legalActions = gameState.getLegalActions(self.index)
		return random.choice(legalActions)









