#!/bin/python3

from itertools import product
import math

#
# Rover movement. Inputs, with placeholders:
#


# 1. Algorithm the program uses => BFS, UCS, A*

algorithm = ""

# 2. Positive integers representing width and height of map

width, height = 0, 0

# 3. Coordinates of the Landing site

landX, landY = 0, 0

# 4. Maximum permissible elevation change

maxDelEle = 0

# 5. Number of target sites

targetNum = 0

# 6. Coordinates of target sites, spread across targetNums lines, will be initialized to an array

targetSites = []

# 7. Elevations of each unit in the map as an array

elevations = []

# Additional helpers

visited = []

# Node queue

nodeQueue = []

# solution paths

solutions = {}


# Define a node
class Node:
    def __init__(self, state, parent, **kwargs):
        self.state = state
        self.parent = parent
        # Misc is used to store the "heuristic" and "cost" of the node in cases like A* or UCS.
        self.misc = kwargs

    
    def __str__(self):
        return "{}".format(self.state)


# Define an enqueueing function
def enqueue(algType, nodes, newNodes, **kwargs):

    miscSortKey = "heuristic" if algType == "A*" else "cost"
    # Get the states of the newer nodes to indentify potential replacements
    newStates = [n.state for n in newNodes]
    inf = float("inf")
    # Identify if newer node has is better than the existing one
    for i in range(len(nodes)):
        # Identify the corresponding node which has the same state as this one. If it exists and it's a better choice
        # discard this node and use that instead.
        currNodeState = nodes[i].state
        # Use get instead of square brackets for exception handling
        if currNodeState in newStates and newNodes[newStates.index(currNodeState)].misc.get(miscSortKey, inf) < nodes[i].misc.get(miscSortKey,inf):
            loc = newStates.index(currNodeState)
            nodes[i] = newNodes[loc]
            del newNodes[loc]
            del newStates[loc]
    nodes.extend(newNodes)
    nodes = sorted(nodes, key=lambda x: x.misc.get(miscSortKey, inf))

    return nodes


# The reachable function, determines if m is reachable from n and vice-versa
def reachable(m, n):
    (mx, my) = m
    (nx, ny) = n
    # Ensure that we aren't looking outside the range of (0, width) and (0, height)
    
    if mx >= width \
        or mx < 0 \
        or nx >= width \
        or nx < 0 \
        or my >= height \
        or my < 0 \
        or ny >= height \
        or ny < 0:
        return False

    # Arrays are indexed as (y, x) instead of the cartesian (x, y)
    return abs(elevations[my][mx] - elevations[ny][nx]) <= maxDelEle


# Get the distance between two points
def distanceBetween(v1, v2):
    return math.sqrt((v1[0] - v2[0])**2 + (v1[1] - v2[1])**2)


# Using a traceback, generate the solution
def processSolution(solution):
    # A list to store the x,y string of each state
    texts = []
    for i in range(len(solution)):
        curr = solution[-i-1]
        texts.append("{},{}".format(curr[0],curr[1]))
    return " ".join(texts)


# Once a goal has been reached, traceback to root, generate the solution and append to solutions
def writeSolution(state):
    now = state
    solution = []
    while now is not None:
        solution.append(now.state)
        now = now.parent
    text = processSolution(solution)
    solutions[state.state] = text

def getNextStates(algType, currentNode, **kwargs):
    # From current coordinates iterate through neighbors to get the next state(s) to add to the nodes list
    currentCoords = currentNode.state
    xNeighbors = [currentCoords[0] - 1, currentCoords[0], currentCoords[0] + 1]
    yNeighbors = [currentCoords[1] - 1, currentCoords[1], currentCoords[1] + 1]
    neighbors = product(xNeighbors, yNeighbors)

    # Return all unvisited, reachable neighbors
    returnable = []
    for n in neighbors:
        # n will exist in visited if n has already been expanded, i.e. there is no need for us to worry about
        # n anymore because the shortest path has been found
        if reachable(n, currentCoords) and n not in visited:
            node = Node(state = n, parent = currentNode)
            returnable.append(node)
    return returnable


def process(algType, nodes, currentNode, **kwargs):
    # Get heuristic in case algorithm is A*, cost otherwise
    if algType == "A*":
       
       # Cost function is the euclidean distance between the node and current node, calculated as the L2 norm of the two vectors
       # Multiply by 10 and get the integral value so that you get 10 and 14 for non-diagonal and diagonal respectively
       # Also add the elevations for 3D cost!
        costFn = lambda x: currentNode.misc.get("cost", 0) \
                + int(distanceBetween(x.state, currentNode.state)*10) \
                + abs(elevations[x.state[1]][x.state[0]] - elevations[currentNode.state[1]][currentNode.state[0]])

        # Define the heuristic function as the minimum euclidean distance between the point and a goal
        # The heuristic function component is run between the point and all targets, the minimum of which is taken
        heuristicFnCompAStar = lambda x, y: distanceBetween(x.state, y)
        for n in nodes:
            n.misc["cost"] = costFn(n)
            n.misc["heuristics"] = [heuristicFnCompAStar(n, t) for t in targetSites]
            n.misc["heuristic"] = n.misc["cost"] + min(n.misc["heuristics"])
            
 
    else:
        # The cost function is just the 2D cost for UCS, number of parents for BFS [used for avoiding cycles]
        costFnUCS = lambda x: currentNode.misc.get("cost", 0) + int(distanceBetween(x.state, currentNode.state)*10)
        costFnBFS = lambda x: currentNode.misc.get("cost", 0) + 1
        for n in nodes:
            n.misc["cost"] = costFnUCS(n) if algType == "UCS" else costFnBFS(n)
        
        
    return nodes


def iterateThroughNodes(algType, startState, **kwargs):
    global targetSites, nodeQueue
    # Start in startNode and initialize nodeQueue
    startNode = Node(state=startState, parent=None)
    nodeQueue.append(startNode)
    # Iterate through nodeQueue
    while len(nodeQueue) > 0:
        value = nodeQueue.pop(0)
        # Append a node to visited only when it is dequeued from the nodeQueue, ensuring that
        # the shortest path is only considered for this.
        visited.append(value.state)

        # If the node we have dequeued is a target
        # Generate the solution trace and remove the it from target sites.
        # BFS, A* and UCS are guaranteed to find the optimal solution
        if value.state in targetSites:
            writeSolution(value)
            goalNumber = targetSites.index(value.state)
            del targetSites[goalNumber]
            # Remove all heuristic indications for that certain goal node
            if algType == "A*":
                for n in nodeQueue:
                    try:
                        n.misc["heuristics"].pop(goalNumber)
                        n.misc["heuristc"] = n.misc["cost"] + min(n.misc["heuristics"])
                    except ValueError:
                        # ValueError is thrown when heuristics are empty, i.e. all goals have been found
                        break
            # If all target sites are found, then the algorithm is successful
            if len(targetSites) == 0:
                return True
        
        # Get the next nodes, an older goal state can also be a throughfare to the new one
        newNodes = getNextStates(algType, value)
        newNodes = process(algType, newNodes, value)
        nodeQueue = enqueue(algType, nodeQueue, newNodes)
    
    # If all reachable nodes have been visited but all targets haven't then it's a failure.
    for t in targetSites:
        solutions[t] = "FAIL"
    return False

def executeAlgorithm(fileName):
    global targetSites, elevations, visited, solutions, nodeQueue, maxDelEle, width, height
    targetSites = []
    elevations = []
    visited = []
    solutions = {}
    nodeQueue = []
    with open("{}.txt".format(fileName)) as input:
        rawdata = input.read()

    lines = [l.strip() for l in rawdata.split("\n")]
    algorithm = lines[0]

    widthAndHeight = lines[1].split(" ")
    width = int(widthAndHeight[0])
    height = int(widthAndHeight[1])

    landingCoordinates = lines[2].split(" ")
    landX = int(landingCoordinates[0])
    landY = int(landingCoordinates[1])
    startState = (landX, landY)

    maxDelEle = int(lines[3])

    targetNum = int(lines[4])

    inputs = []
    for i in range(targetNum):
        line = lines[5+i]
        coords = line.split(" ")
        currTarget = (int(coords[0]), int(coords[1]))
        inputs.append(currTarget)
        solutions[currTarget] = ""
    # multiple inputs can correspond to a single target site
    targetSites = [s for s in solutions.keys()]

    startAnchor = targetNum + 5
    for i in range(height):
        line = lines[startAnchor + i]
        currentRow = [int(x) for x in line.split(" ")]
        elevations.append(currentRow)

    outputName = fileName.replace("input", "output")
    iterateThroughNodes(algorithm, startState)
    with open("{}.txt".format(outputName), "w") as out:
        out.write("\n".join([solutions[i] for i in inputs]))
        return solutions