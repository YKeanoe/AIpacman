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
  """
  This function should return a list of two agents that will form the
  team, initialized using firstIndex and secondIndex as their agent
  index numbers.  isRed is True if the red team is being created, and
  will be False if the blue team is being created.

  As a potentially helpful development aid, this function can take
  additional string-valued keyword arguments ("first" and "second" are
  such arguments in the case of this function), which will come from
  the --redOpts and --blueOpts command-line arguments to capture.py.
  For the nightly contest, however, your team will be created without
  any extra arguments, so you should make sure that the default
  behavior is what you want for the nightly contest.
  """

  # The following line is an example only; feel free to change it.
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
		while len(agentsTeam) < (angetsLen/2):
			agentsTeam.append(i)
			i += 2
			if i >= agentsLen:
				i = 0
		agentsTeam.sort()
		self.registerTeam(agentsTeam)

	def expectiminimax(self, gameState, agent, mdepth):
		if agent >= gameState.getNumAgents():
			agent = 0
			mdepth += 1

		if mdepth == 2 or gameState.isOver()
			return self.evaluationFunction(gameState)

		legalActions = gameState.getLegalActions(agent)
		if agent in self.agentsOnTeam
			v = float("-inf")
			for action in legalActions:
				v = max(v, self.expectiminimax(gameState.generateSuccessor(agent, action), agent + 1,mdepth))
			return v
		else:
			v = []
			prob = 1.0/len(legalActions)
			for action in legalActions:
				expectVals = self.expectiminimax(gameState.generateSuccessor(agent, action), agent + 1,mdepth)
				v.append(expectVals)
			ret = sum(v)/len(legalActions)
			return ret


class OffensiveAgent(ExpectimaxAgent):

	def chooseAction(self, gameState):	
		v = []
		legalActions = gameState.getLegalActions(self.index)
		for action in legalActions:
			expectVals = self.expectiminimax(gameState.generateSuccessor(self.index,action),self.index+1,0)
			v.append((expectVals, action))
		vBestScore = max(v)
		bestIndices = [index for index in range(len(v)) if v[index] == vBestScore]
		chosenIndex = random.choice(bestIndices) # Pick randomly among the best
		return v[chosenIndex][1]

	def evaluate(currentGameState):
		"""
		Score = 1 * currentScore
				- 1 * distance to closest food
				- 2 * distance to closest non scared ghost
				- 20 * distance to closest capsule
		"""

		newPos = currentGameState.getAgentPosition(self.index)
		newFood = self.getFood()

		newGhostStates = currentGameState.getGhostStates()
		newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
		newCapsules = currentGameState.getCapsules()
	
		foodDistance = []
		ghostDistance = []
		foodList = currentGameState.getFood().asList()
		pacmanPos = list(currentGameState.getPacmanPosition())
		
		score = self.getScore()
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
			score -= 0.5 * manhattanDistance(food,pacmanPos)
	
		
		for capsule in newCapsules:
			score -= 2 * manhattanDistance(capsule,pacmanPos)
	
		return score









