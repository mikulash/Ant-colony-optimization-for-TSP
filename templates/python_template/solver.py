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
    path = [0]

    notVisitedPoints = listOfPlaces.copy()
    pathLength = 0
    currentPoint = random.choice(listOfPlaces)
    print('currPoint', currentPoint)
    while len(notVisitedPoints) > 0:
        nextPoint = getNextEdge(currentPoint, notVisitedPoints, path)
        print('nextPoint', nextPoint)
        path.append(nextPoint)
        if nextPoint == path[0]:
            break
        notVisitedPoints.remove(nextPoint)
        pathLength += distanceMatrix[path[-1]][nextPoint]
        currentPoint = nextPoint

    print('ant goes through graph')
    return path, pathLength


def getNextEdge(currentPoint, notVisitedPoints, walkedPath):
    weights = []
    for i in range(len(notVisitedPoints)):
        weights.append(pheromoneMatrix[currentPoint][notVisitedPoints[i]] + (1 / distanceMatrix[currentPoint][notVisitedPoints[i]]))
    return currentPoint + 1


def evaporatePheromones(pheromoneMatrix, rate=0.5):
    for i in range(len(pheromoneMatrix)):
        for j in range(len(pheromoneMatrix)):
            pheromoneMatrix[i][j] *= rate


def createPheromoneMatrix(distanceMatrix):
    pheromoneMatrix = []
    for i in range(len(distanceMatrix)):
        row = []
        for j in range(len(distanceMatrix)):
            row.append(1)
        pheromoneMatrix.append(row)
    return pheromoneMatrix


def ACO(coordinates, distanceMatrix):
    antsCount = 5
    pheromoneMatrix = createPheromoneMatrix(distanceMatrix)
    listOfPlaces = list(range(len(coordinates)))
    print(listOfPlaces)
    for ant in range(antsCount):
        antGoesThroughGraph(listOfPlaces, distanceMatrix, pheromoneMatrix)
    # releaseTheAnts(antsCount, pheromoneMatrix, distanceMatrix)
    evaporatePheromones(pheromoneMatrix)
    # updatePheromones()
    return True


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
