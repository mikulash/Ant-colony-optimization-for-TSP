import random
import sys
import json
from datetime import datetime

instance_path = sys.argv[1]
output_path = sys.argv[2]


def createRandomPath(points):
    # create starting point by random shuffling indexes of places
    path = list(range(len(points)))
    random.shuffle(path)
    print('rand', path)
    return path


def getPathLength(points, matrix):
    # get path length from euclidean 2d matrix
    length = 0
    for i in range(len(points)):
        if i == 0:
            continue
        length += matrix[points[i - 1]][points[i]]
    return length


def getNeighbors(path):
    # get all neighbors of current path by swapping two  points
    neighbors = []
    for i in range(len(path)):
        for j in range(i + 1, len(path)):
            neighbor = path.copy()
            neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
            neighbors.append(neighbor)
    return neighbors


def findBestPath(neighbors, matrix):
    # find the best neighbor by comparing path lengths
    best = neighbors[0]
    for i in range(len(neighbors)):
        if getPathLength(neighbors[i], matrix) < getPathLength(best, matrix):
            best = neighbors[i]
    return best


def hillClimbing(coordinates, matrix):
    bestPath = createRandomPath(coordinates)
    bestPathLength = getPathLength(bestPath, matrix)
    while True:
        pathNeighbors = getNeighbors(bestPath)
        bestNeighbor = findBestPath(pathNeighbors, matrix)
        bestNeighborLength = getPathLength(bestNeighbor, matrix)
        if bestNeighborLength > bestPathLength:
            return bestPath
        else:
            bestPath = bestNeighbor
            bestPathLength = bestNeighborLength


# ant colony optimization
def antGoesThroughGraph(listOfPlaces, distanceMatrix, pheromoneMatrix):
    notVisitedPoints = listOfPlaces.copy()
    currentPoint = random.choice(notVisitedPoints)  # start from random point
    visited = [currentPoint]
    while len(notVisitedPoints) > 1:
        notVisitedPoints.remove(currentPoint)
        nextPoint = getNextEdge(currentPoint, notVisitedPoints, pheromoneMatrix, distanceMatrix)
        visited.append(nextPoint)
        currentPoint = nextPoint
    visited.append(visited[0])  # return to starting point
    return visited


def getNextEdge(currentPoint, notVisitedPoints, pheromoneMatrix, distanceMatrix):
    weights = []
    BETA = 1.1
    ALPHA = 1.1
    for i in range(len(notVisitedPoints)):
        pheromones = pheromoneMatrix[currentPoint][notVisitedPoints[i]]
        distance = distanceMatrix[currentPoint][notVisitedPoints[i]]
        weights.append(pheromones ** ALPHA * (1 / distance) ** BETA)
    weightSum = sum(weights)
    attractivity = [weight / weightSum for weight in weights]  # p^k_xy
    nextPoint = random.choices(notVisitedPoints, attractivity)[0]
    return nextPoint


def evaporatePheromones(pheromoneMatrix, evaporation=0.3):
    for i in range(len(pheromoneMatrix)):
        for j in range(len(pheromoneMatrix)):
            pheromoneMatrix[i][j] *= evaporation


def updatePheromones(paths, pheromoneMatrix, distanceMatrix):
    evaporation = 0.5
    Q = 50
    for path in paths:
        pheromoneAmount = Q / getPathLength(path, distanceMatrix)
        for i in range(len(path)):
            if i == 0:
                continue
            pheromoneMatrix[path[i - 1]][path[i]] += pheromoneAmount
            pheromoneMatrix[path[i]][path[i - 1]] += pheromoneAmount
    evaporatePheromones(pheromoneMatrix, evaporation)


def createPheromoneMatrix(distanceMatrix):
    pheromoneMatrix = []
    for i in range(len(distanceMatrix)):
        row = []
        for j in range(len(distanceMatrix)):
            if i == j:
                row.append(0)
            else:
                row.append(1)
        pheromoneMatrix.append(row)
    return pheromoneMatrix


def doesArrayStartToConverge(arr):
    if len(arr) < 5:
        return False
    lastCoupleOfValues = arr[-10:-2]
    lastValue = arr[-1]
    for i in range(len(lastCoupleOfValues)):
        if abs(lastCoupleOfValues[i] - lastValue) < 10:
            return True
    return False


def ACO(coordinates, distanceMatrix, timeout, iterations=100, antsCount=50):
    start = datetime.now()
    pheromoneMatrix = createPheromoneMatrix(distanceMatrix)
    listOfPlaces = list(range(len(coordinates)))
    paths = []
    bestPathLengths = []
    for i in range(iterations):
        paths = []
        for ant in range(antsCount):
            path = antGoesThroughGraph(listOfPlaces, distanceMatrix, pheromoneMatrix)
            paths.append(path)
        updatePheromones(paths, pheromoneMatrix, distanceMatrix)
        bestPathLengths.append(getPathLength(findBestPath(paths, distanceMatrix), distanceMatrix))
        if doesArrayStartToConverge(bestPathLengths):
            print('converged at iteration', i)
            break
        if (datetime.now() - start).total_seconds() > timeout:
            print('timeout')
            break

    bestPath = findBestPath(paths, distanceMatrix)  # reused function from hillclimbing, finds the shortest path
    return bestPath


with open(instance_path) as f:
    instance = json.load(f)
    aco = True  # select algorithm
    if aco:
        # ants colonization algorithm
        solution = ACO(instance['Coordinates'], instance['Matrix'], instance['Timeout'])
    else:
        solution = hillClimbing(instance['Coordinates'], instance['Matrix'])
    print(solution)
    with open(output_path, 'w') as f:
        json.dump(solution, f)
