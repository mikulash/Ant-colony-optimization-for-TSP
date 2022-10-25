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


with open(instance_path) as f:
    instance = json.load(f)
    print(instance.keys())
    solution = hillClimbing(instance['Coordinates'], instance['Matrix'])
    print(solution)
    with open(output_path, 'w') as f:
        json.dump(solution, f)
