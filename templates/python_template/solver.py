import random
import sys
import json

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
            # print('xxxx', neighbor)
            neighbors.append(neighbor)
    # print('neig', neighbors[10])
    # print(len(neighbors))
    return neighbors


def findBestNeighbor(neighbors, matrix):
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
        bestNeighbor = findBestNeighbor(pathNeighbors, matrix)
        bestNeighborLength = getPathLength(bestNeighbor, matrix)
        if bestNeighborLength > bestPathLength:
            return bestPath
        else:
            bestPath = bestNeighbor
            bestPathLength = bestNeighborLength


# ant colony optimization
def antGoesThroughGraph(listOfPlaces, distanceMatrix, pheromoneMatrix):
    visited = [0]
    notVisitedPoints = listOfPlaces.copy()
    # currentPoint = random.choice(notVisitedPoints)  # start from random point
    currentPoint = 0  # start from random point
    # >2 because one node is deleted in the step and then there is only the beginning node left
    while len(notVisitedPoints) > 2:
        notVisitedPoints.remove(currentPoint)
        nextPoint = getNextEdge(currentPoint, notVisitedPoints, pheromoneMatrix, distanceMatrix)
        visited.append(nextPoint)
        currentPoint = nextPoint
    visited.append(visited[0])  # return to starting point
    return visited


def getNextEdge(currentPoint, notVisitedPoints, pheromoneMatrix, distanceMatrix):
    weights = []
    BETA = 1.1
    print(notVisitedPoints)
    for i in range(len(notVisitedPoints)):
        pheromones = pheromoneMatrix[currentPoint][notVisitedPoints[i]]
        distance = distanceMatrix[currentPoint][notVisitedPoints[i]]
        weights.append(pheromones * (1/distance)**BETA)
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
        pheromoneAmmount = Q / getPathLength(path, distanceMatrix)
        print('pat', path)
        print('xxx',pheromoneAmmount)
        for i in range(len(path)):
            if i == 0:
                continue
            pheromoneMatrix[path[i - 1]][path[i]] += pheromoneAmmount
            pheromoneMatrix[path[i - 1]][path[i]] = round(pheromoneMatrix[path[i - 1]][path[i]], 1)
            pheromoneMatrix[path[i]][path[i - 1]] += pheromoneAmmount
            pheromoneMatrix[path[i]][path[i - 1]] = round(pheromoneMatrix[path[i]][path[i - 1]], 1)
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


def ACO(coordinates, distanceMatrix):
    antsCount = 20
    pheromoneMatrix = createPheromoneMatrix(distanceMatrix)
    print(pheromoneMatrix)
    listOfPlaces = list(range(len(coordinates)))
    print(listOfPlaces)
    iterations = 30
    for i in range(iterations):
        paths = []
        for ant in range(antsCount):
            path = antGoesThroughGraph(listOfPlaces, distanceMatrix, pheromoneMatrix)
            paths.append(path)
        print(paths)
        updatePheromones(paths, pheromoneMatrix, distanceMatrix)

    print('**********')
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in pheromoneMatrix]))

    return paths[-1]


with open(instance_path) as f:
    instance = json.load(f)
    aco = True
    if aco:
        solution = ACO(instance['Coordinates'], instance['Matrix'])
    else:
        solution = hillClimbing(instance['Coordinates'], instance['Matrix'])
    print(solution)
    with open(output_path, 'w') as f:
        json.dump(solution, f)
