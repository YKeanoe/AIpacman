# search.py
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

import time

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
#        util.raiseNotDefined()
        print "start state from search.py"

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()

def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    "util.raiseNotDefined()"

    from game import Directions
    from util import Stack

    print "\n"

    current = problem.getStartState()
    previous = None
 
    explored = [(current)]
    
    """
    Nodes is a list of dictionary to store the previous nodes, action, and if the node is expanded/traveled
    """
    nodes = []
    nodes.append({'Current': current, 'Previous': None, 'Action': None, 'Traveled': False})
    
    stack = Stack()
    stack.push(current)

    while not stack.isEmpty():
        current = stack.pop()
        print "Current: ", current
        explored.append((current))
        currNode = []
        for item in nodes:
            if item['Current'] == current:
                print "Current node found: ", item
                currNode.append(item)

        if len(currNode) > 1:
            print "CurrNode bigger than 1"
            for item in currNode:
                print "Item ", item
                print "Prev ", previous
                if item['Previous'] == previous:
                    item['Traveled'] = True
        else:
            print "CurrNode just 1"
            currNode[0]['Traveled'] = True

        print "currNode: ", currNode           
        previous = current

        if problem.isGoalState(current):
            break

        successors = problem.getSuccessors(current)
        for successor in successors:
            if successor[0] not in explored:
                print "Successor: ", successor
                nodes.append({'Current': successor[0], 'Previous': current, 'Action': successor[1], 'Traveled': False})
                stack.push(successor[0])
    path = []
    pathCur = nodes[-1]

    while pathCur:
        print "pathCur = ", pathCur
        if not pathCur['Previous']:
            break
        path.insert(0, pathCur['Action'])
        pathCur = next((item for item in nodes if item['Current'] == pathCur['Previous'] and item['Traveled'] ), None)

    #print path
    #print nodes

    return path

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    "util.raiseNotDefined()"

    from game import Directions
    from util import Queue

    print "\n"

    current = problem.getStartState()
    explored = []
    
    """
    Nodes is a list of dictionary to store the previous nodes, action, and if the node is expanded/traveled
    """
    nodes = []
    nodes.append({'Current': current, 'Previous': None, 'Action': None, 'Traveled': False})
    
    stack = Queue()
    stack.push(current)

    pathCur = None

    while not stack.isEmpty():
        current = stack.pop()
        print "Current: ", current
        if current in explored:
            continue

        explored.append((current))

        currNode = next((item for item in nodes if item['Current'] == current), None)

        print "Current node found: ", currNode

        currNode['Traveled'] = True
        print "currNode: ", currNode           

#        previous = current

        if problem.isGoalState(current):
#           pathCur = next((item for item in currNode if item['Traveled'] ), None)
            pathCur = currNode
            break

        successors = problem.getSuccessors(current)
        for successor in successors:
            if successor[0] not in explored:
                print "Successor: ", successor
                nodes.append({'Current': successor[0], 'Previous': current, 'Action': successor[1], 'Traveled': False})
                stack.push(successor[0])
    path = []
#    pathCur = nodes[-1]

    while pathCur:
        print "pathCur = ", pathCur
        if not pathCur['Previous']:
            break
        path.insert(0, pathCur['Action'])
        pathCur = next((item for item in nodes if item['Current'] == pathCur['Previous'] and item['Traveled'] ), None)

    #print path
    #print nodes

    return path

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    "util.raiseNotDefined()"

    from game import Directions
    from util import PriorityQueue

    print "\n"

    current = problem.getStartState()
    explored = []
    
    """
    Nodes is a list of dictionary to store the previous nodes, action, and if the node is expanded/traveled
    """
    nodes = []
    nodes.append({'Current': current, 'Previous': None, 'Action': None, 'Traveled': False, 'Cost': 0})
    
    stack = PriorityQueue()
    stack.push(current,0)

    pathCur = None

    while not stack.isEmpty():
        current = stack.pop()
        print "Current: ", current
        if current in explored:
            continue

        explored.append((current))

        potentialNodes = []
        currentNode = None
        for item in nodes:
            if item['Current'] == current:
                print "Current node found: ", item
                potentialNodes.append(item)

        if len(potentialNodes) > 1:
            print "CurrNode bigger than 1"
            print "Prev ", previous              
            smallNode = potentialNodes[0]
            for item in potentialNodes:
                print "Item ", item
                if smallNode['Cost'] > item['Cost']:
                    smallNode = item
            currNode = smallNode
#                if item['Previous'] == previous:
#                    currNode = item
#                    item['Traveled'] = True
        else:
            print "CurrNode just 1"
            currNode = potentialNodes[0]
#            currNode[0]['Traveled'] = True

#       currNode = next((item for item in nodes if item['Current'] == current), None)

        print "Current final node found: ", currNode

        currNode['Traveled'] = True
        print "currNode: ", currNode           

        previous = current

        if problem.isGoalState(current):
#           pathCur = next((item for item in currNode if item['Traveled'] ), None)
            pathCur = currNode
            break

        successors = problem.getSuccessors(current)
        for successor in successors:
            if successor[0] not in explored:
                print "Successor: ", successor
                costSoFar = successor[2] + currNode['Cost']
                nodes.append({'Current': successor[0], 'Previous': current, 'Action': successor[1], 'Traveled': False, 'Cost': costSoFar })
                stack.push(successor[0],costSoFar)
    path = []
#    pathCur = nodes[-1]

    while pathCur:
        print "pathCur = ", pathCur
        if not pathCur['Previous']:
            break
        path.insert(0, pathCur['Action'])
        potentialPath = []
        for item in nodes:
            if item['Current'] == pathCur['Previous'] and item['Traveled']:
                potentialPath.append(item)

        if len(potentialPath) > 1:
            print "potential path more than 1"
            pathCur = potentialPath[0]
            for item in potentialPath:
                if pathCur['Cost'] > item['Cost']:
                    pathCur = item
        else:
            print "potential path just 1"
            pathCur = potentialPath[0]

#        pathCur = next((item for item in nodes if item['Current'] == pathCur['Previous'] and item['Traveled'] ), None)

    #print path
    #print nodes

    return path

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    "util.raiseNotDefined()"
 
    from game import Directions
    from util import PriorityQueue
    from searchAgents import manhattanHeuristic

    print "\n"

    current = problem.getStartState()
    explored = []
    
    """
    Nodes is a list of dictionary to store the previous nodes, action, and if the node is expanded/traveled
    """
    nodes = []
    nodes.append({'Current': current, 'Previous': None, 'Action': None, 'Traveled': False, 'Cost': 0})
    
    stack = PriorityQueue()
    stack.push(current,0)

    pathCur = None

    while not stack.isEmpty():
        current = stack.pop()
        print "Current: ", current
        testHeu = heuristic(current,problem)
        print "testHeu : ", testHeu
        if current in explored:
            continue

        explored.append((current))

        potentialNodes = []
        currentNode = None
        for item in nodes:
            if item['Current'] == current:
                print "Current node found: ", item
                potentialNodes.append(item)

        if len(potentialNodes) > 1:
            print "CurrNode bigger than 1"
            print "Prev ", previous              
            smallNode = potentialNodes[0]
            for item in potentialNodes:
                print "Item ", item
                if smallNode['Cost'] > item['Cost']:
                    smallNode = item
            currNode = smallNode
#                if item['Previous'] == previous:
#                    currNode = item
#                    item['Traveled'] = True
        else:
            print "CurrNode just 1"
            currNode = potentialNodes[0]
#            currNode[0]['Traveled'] = True

#       currNode = next((item for item in nodes if item['Current'] == current), None)

        print "Current final node found: ", currNode

        currNode['Traveled'] = True
        print "currNode: ", currNode           

        previous = current

        if problem.isGoalState(current):
#           pathCur = next((item for item in currNode if item['Traveled'] ), None)
            pathCur = currNode
            break

        successors = problem.getSuccessors(current)
        for successor in successors:
            if successor[0] not in explored:
                print "Successor: ", successor
                costSoFar = successor[2] + currNode['Cost']
                costPlusHeuristic = costSoFar + heuristic(successor[0],problem)
                nodes.append({'Current': successor[0], 'Previous': current, 'Action': successor[1], 'Traveled': False, 'Cost': costSoFar })
                stack.push(successor[0],costPlusHeuristic)
    path = []
#    pathCur = nodes[-1]

    while pathCur:
        print "pathCur = ", pathCur
        if not pathCur['Previous']:
            break
        path.insert(0, pathCur['Action'])
        potentialPath = []
        for item in nodes:
            if item['Current'] == pathCur['Previous'] and item['Traveled']:
                potentialPath.append(item)

        if len(potentialPath) > 1:
            print "potential path more than 1"
            pathCur = potentialPath[0]
            for item in potentialPath:
                if pathCur['Cost'] > item['Cost']:
                    pathCur = item
        else:
            print "potential path just 1"
            pathCur = potentialPath[0]

#        pathCur = next((item for item in nodes if item['Current'] == pathCur['Previous'] and item['Traveled'] ), None)

    #print path
    #print nodes
    return path
   

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
