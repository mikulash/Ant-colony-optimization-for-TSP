import random
import sys
import json

instance_path = sys.argv[1]
output_path = sys.argv[2]

def createRandomPath(points):
    # create starting point by random shuffling indexes of places
    path = list(range(len(points)))
    print('path', path)
    random.shuffle(path)
    print('rand', path)
    return path


def getPathLength(points, matrix):
    # get path length from euclidean 2d matrix
    length = 0
    # print(matrix)
    for i in range(len(points)):
        if i == 0:
            continue
        # print(i, points[i-1], points[i], matrix[points[i-1]][points[i]])
        length += matrix[points[i-1]][points[i]]
    return length


def getNeighbors(path):
    # get all neighbors of current path by swapping two  points
    # print(path)
    neighbors = []
    for i in range(len(path)):
        for j in range(i+1, len(path)):
            neighbor = path.copy()
            neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
            # print('xxxx', neighbor)
            neighbors.append(neighbor)
    # print('neig', neighbors[10])
    # print(len(neighbors))
    return neighbors

def findBestNeighbor(neighbors, matrix):
    # find the best neighbor by comparing path lengths
    for i in range(len(neighbors)):
        if i == 0:
            best = neighbors[i]
            continue
        if getPathLength(neighbors[i], matrix) < getPathLength(best, matrix):
            best = neighbors[i]
    print('best', best)
    return best


def conditionSatisfied(currentPath, bestNeighbor, matrix):
    # check if current path is better than best neighbor
    if getPathLength(currentPath, matrix) <= getPathLength(bestNeighbor, matrix):
        return currentPath
    else:
        return bestNeighbor


def hillClimbing():
    pass

with open(instance_path) as f:
    instance = json.load(f)
    print(instance.keys())
    randomPath = createRandomPath(instance['Coordinates'])
    randomPathLength = getPathLength(randomPath, instance['Matrix'])
    pathNeighbors = getNeighbors(randomPath)
    bestNeighbor = findBestNeighbor(pathNeighbors, instance['Matrix'])
    # print(randomPathLength)

sol = [i for i in range(len(instance['Matrix']))]

with open(output_path, 'w') as f:
    json.dump(sol, f)
