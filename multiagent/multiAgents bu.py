# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
	"""
	  A reflex agent chooses an action at each choice point by examining
	  its alternatives via a state evaluation function.

	  The code below is provided as a guide.  You are welcome to change
	  it in any way you see fit, so long as you don't touch our method
	  headers.
	"""


	def getAction(self, gameState):
		"""
		You do not need to change this method, but you're welcome to.

		getAction chooses among the best options according to the evaluation function.

		Just like in the previous project, getAction takes a GameState and returns
		some Directions.X for some X in the set {North, South, West, East, Stop}
		"""
		# Collect legal moves and successor states
		legalMoves = gameState.getLegalActions()

		# Choose one of the best actions
		scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
		bestScore = max(scores)
		bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
		chosenIndex = random.choice(bestIndices) # Pick randomly among the best

		"Add more of your code here if you want to"

		return legalMoves[chosenIndex]

	def evaluationFunction(self, currentGameState, action):
		"""
		Design a better evaluation function here.

		The evaluation function takes in the current and proposed successor
		GameStates (pacman.py) and returns a number, where higher numbers are better.

		The code below extracts some useful information from the state, like the
		remaining food (newFood) and Pacman position after moving (newPos).
		newScaredTimes holds the number of moves that each ghost will remain
		scared because of Pacman having eaten a power pellet.

		Print out these variables to see what you're getting, then combine them
		to create a masterful evaluation function.
		"""
		# Useful information you can extract from a GameState (pacman.py)
		successorGameState = currentGameState.generatePacmanSuccessor(action)
		newPos = successorGameState.getPacmanPosition()
		newFood = successorGameState.getFood()
		newGhostStates = successorGameState.getGhostStates()
		newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

		"*** YOUR CODE HERE ***"
		"""
		Using manhattanDistane algorithm to calculate the closest food and ghosts.
		Since the higher the returned score is the better, convert the food manhattan
		distance value to minus to get the best option. The manhattan distance for ghosts
		isn't changed and the pacman will move away from the ghost if the distance is
		less than 2.
		"""
		if action == 'Stop':
			return float('-inf')

		foodDistance = []
		ghostDistance = []
		foodList = currentGameState.getFood().asList()
		pacmanPos = list(successorGameState.getPacmanPosition())

		ghostDistance = [manhattanDistance(ghost.getPosition(),pacmanPos)\
						for ghost in newGhostStates if ghostState.scaredTimer == 0]

		for ghostDist in ghostDistance:
			if ghostDist < 2:
				return float('-inf')

		foodDistance = [ -1 * manhattanDistance(food,pacmanPos) for food in foodList]
		return max(foodDistance)

def scoreEvaluationFunction(currentGameState):
	"""
	  This default evaluation function just returns the score of the state.
	  The score is the same one displayed in the Pacman GUI.

	  This evaluation function is meant for use with adversarial search agents
	  (not reflex agents).
	"""
	return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
	"""
	  This class provides some common elements to all of your
	  multi-agent searchers.  Any methods defined here will be available
	  to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

	  You *do not* need to make any changes here, but you can if you want to
	  add functionality to all your adversarial search agents.	Please do not
	  remove anything, however.

	  Note: this is an abstract class: one that should not be instantiated.  It's
	  only partially specified, and designed to be extended.  Agent (game.py)
	  is another abstract class.
	"""

	def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
		self.index = 0 # Pacman is always agent index 0
		self.evaluationFunction = util.lookup(evalFn, globals())
		self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
	"""
	  Your minimax agent (question 2)
	"""

	def getAction(self, gameState):
		"""
		  Returns the minimax action from the current gameState using self.depth
		  and self.evaluationFunction.

		  Here are some method calls that might be useful when implementing minimax.

		  gameState.getLegalActions(agentIndex):
			Returns a list of legal actions for an agent
			agentIndex=0 means Pacman, ghosts are >= 1

		  gameState.generateSuccessor(agentIndex, action):
			Returns the successor game state after an agent takes an action

		  gameState.getNumAgents():
			Returns the total number of agents in the game
		"""
		"*** YOUR CODE HERE ***"
		"util.raiseNotDefined()"

		# print "Start"
		minimaxVals = []
		minimaxVals.append((float('-inf'), 'None'))

		legalActions = gameState.getLegalActions(0)
		for action in legalActions:
			if action == 'Stop':
				minimaxVals.append((float('-inf'), 'Stop'))
			else:
				v = self.minimax(gameState.generateSuccessor(0,action), 1, 0)
				minimaxVals.append((v, action))
		return max(minimaxVals)[1]

	def minimax(self, gameState, agent, mdepth):
		if agent >= gameState.getNumAgents():
			agent = 0
			mdepth += 1

		if mdepth == self.depth:
			return self.evaluationFunction(gameState)

		if agent == 0:
			return self.max_value(gameState, agent, mdepth)
		else:
			return self.min_value(gameState, agent, mdepth)

	def max_value(self, gameState, agent, mdepth):
		minimaxVals = []
		minimaxVals.append((-9999, 'None'))

		if not gameState.getLegalActions(agent):
			return self.evaluationFunction(gameState)

		legalActions = gameState.getLegalActions(agent)
		for action in legalActions:
			if action == 'Stop':
				minimaxVals.append((-9999, 'Stop'))
			else:
				v = self.minimax(gameState.generateSuccessor(agent,action), agent+1, mdepth)
				minimaxVals.append((v, action))
		return max(minimaxVals)[0]

	def min_value(self, gameState, agent, mdepth):
		minimaxVals = []
		minimaxVals.append((9999, 'None'))

		#print "min depth {0} for agent {1}".format(mdepth, agent)

		if not gameState.getLegalActions(agent):
			return self.evaluationFunction(gameState)

		legalActions = gameState.getLegalActions(agent)
		for action in legalActions:
			v = self.minimax(gameState.generateSuccessor(agent,action), agent+1, mdepth)
			# print "For {0} value is {1}".format(action, v)
			minimaxVals.append((v, action))
			# minimaxVals.append((self.min_value(gameState.generateSuccessor(agent,action), agent+1, currentDepth ), action))
		# print "MIN"
		# print minimaxVals
		# print min(minimaxVals)[0]
		return min(minimaxVals)[0]


class AlphaBetaAgent(MultiAgentSearchAgent):
	"""
	  Your minimax agent with alpha-beta pruning (question 3)
ne'), ((9999, 'None'), 'Left'), ((9999, 'None'), 'Right')]

	"""

	def getAction(self, gameState):
		"""
		  Returns the minimax action using self.depth and self.evaluationFunction
		"""
		"*** YOUR CODE HERE ***"
		"util.raiseNotDefined()"
		"""
		Comparing alhpa and beta is < and > not >= or <=
		"""
		v = (float("-inf"), 'None')
		alpha = float('-inf')
		beta = float('inf')
		legalActions = gameState.getLegalActions(0)
		for action in legalActions:
			if action == "Stop":
				continue
			v = max(v, (self.alphabeta(gameState.generateSuccessor(0, action), 1, 0, alpha, beta), action))
			if v[0] > beta:
				return v[1]
			alpha = max(alpha, v[0])
		return v[1]

	def alphabeta(self, gameState, agent, mdepth, alpha, beta):
		if agent >= gameState.getNumAgents():
			agent = 0
			mdepth += 1

		if mdepth == self.depth or gameState.isWin() or gameState.isLose():
			return self.evaluationFunction(gameState)

		legalActions = gameState.getLegalActions(agent)
		if agent == 0:
			v = float("-inf")
			for action in legalActions:
				if action == "Stop":
					continue
				v = max(v, self.alphabeta(gameState.generateSuccessor(agent, action), agent + 1,mdepth, alpha, beta))
				if v > beta:
					return v
				alpha = max(alpha, v)
			return v
		else:
			v = float("inf")
			for action in legalActions:
				if action == "Stop":
					continue
				v = min(v, self.alphabeta(gameState.generateSuccessor(agent, action), agent + 1,mdepth, alpha, beta))
				if v < alpha:
					return v
				beta = min(beta, v)
			return v

class ExpectimaxAgent(MultiAgentSearchAgent):
	"""
	  Your expectimax agent (question 4)
	"""

	def getAction(self, gameState):
		"""
		  Returns the expectimax action using self.depth and self.evaluationFunction

		  All ghosts should be modeled as choosing uniformly at random from their
		  legal moves.
		"""
		"*** YOUR CODE HERE ***"
		"util.raiseNotDefined()"
		#v = (float("-inf"), 'None')
		v = []
		v.append((float("-inf"), 'None'))
		
		legalActions = gameState.getLegalActions(0)
		for action in legalActions:
			if action == "Stop":
				continue
			expectVals = self.expectiminimax(gameState.generateSuccessor(0,action),1,0)
			#print "{0} - {1}".format(action, expectVals)
			# v = max(v, (self.expectiminimax(gameState.generateSuccessor(0, action), 1, 0), action))
			#v = max(v, (expectVals , action))
			v.append((expectVals, action))
		bestScore = max(v)
		bestIndices = [index for index in range(len(v)) if v[index] == bestScore]
		chosenIndex = random.choice(bestIndices) # Pick randomly among the best

		#print v
		#print v[chosenIndex]
		return v[chosenIndex][1]

	def expectiminimax(self, gameState, agent, mdepth):
		if agent >= gameState.getNumAgents():
			agent = 0
			mdepth += 1

		if mdepth == self.depth or gameState.isWin() or gameState.isLose():
			return self.evaluationFunction(gameState)

		legalActions = gameState.getLegalActions(agent)
		if agent == 0:
			v = float("-inf")
			for action in legalActions:
				if action == "Stop":
					continue
				v = max(v, self.expectiminimax(gameState.generateSuccessor(agent, action), agent + 1,mdepth))
			return v
		else:
			#v = float("inf")
			v = []
			prob = 1.0/len(legalActions)
			for action in legalActions:
				expectVals = self.expectiminimax(gameState.generateSuccessor(agent, action), agent + 1,mdepth)
				v.append(expectVals)
				#expectVals = expectVals * prob
				#print expectVals
				#v = min(v, expectVals)
				#print v
			ret = sum(v)/len(legalActions)
			#print ret
			return ret


def betterEvaluationFunction(currentGameState):
	"""
	  Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
	  evaluation function (question 5).

	  DESCRIPTION: <write something here so we know what you did>
	"""
	"*** YOUR CODE HERE ***"
	"util.raiseNotDefined()"
	"""
	Score = 1 * currentScore
			- 1 * distance to closest food
			- 2 * distance to closest non scared ghost
			- 20 * distance to closest capsule
	"""

	newPos = currentGameState.getPacmanPosition()
	newFood = currentGameState.getFood()
	newGhostStates = currentGameState.getGhostStates()
	newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
	newCapsules = currentGameState.getCapsules()

	foodDistance = []
	ghostDistance = []
	foodList = currentGameState.getFood().asList()
	pacmanPos = list(currentGameState.getPacmanPosition())
	
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
			score += -1 * dist

	for food in foodList:
		score -=  manhattanDistance(food,pacmanPos)

	
	for capsule in newCapsules:
		score -= 2 * manhattanDistance(capsule,pacmanPos)
	
	return score


# Abbreviation
better = betterEvaluationFunction

