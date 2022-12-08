import networkx as nx
import numpy as np
from itertools import combinations
from math import sqrt


# Generates the instances of TSP. Two complete undirected graphs with n vertices, the first with
# edges weighted according to euclidean distance and the second according to manhattan distance.
def genTspInput(numNodes, seed):
    np.random.seed(seed)
    nodes = np.random.randint(1000 ,size=(numNodes, 2))
    G = nx.Graph()
    manhattanG = nx.Graph()
    euclideanG = nx.Graph()
    nodeKey = 0

    for n in nodes:
        G.add_node(nodeKey, pos=(n[0], n[1]))
        manhattanG.add_node(nodeKey, pos=(n[0], n[1]))
        euclideanG.add_node(nodeKey, pos=(n[0], n[1]))
        nodeKey += 1

    allNodes = G.nodes()
    allEdges = list(combinations(allNodes, 2))
    for edge in allEdges:
        u = edge[0]
        v = edge[1]
        pos_u = G.nodes[u]['pos']
        pos_v = G.nodes[v]['pos']
        distMan = manhattanDistance(pos_u, pos_v)
        distEuc = euclideanDistance(pos_u, pos_v)
        manhattanG.add_edge(u, v, weight=distMan)    
        euclideanG.add_edge(u, v, weight=distEuc)

    return(euclideanG, manhattanG)

def euclideanDistance(nodeA, nodeB):
    dist = sqrt(pow((nodeB[0] - nodeA[0]),2) + pow((nodeB[1] - nodeA[1]),2))
    return dist


def manhattanDistance(nodeA, nodeB):
    dist = abs(nodeA[0] - nodeB[0]) + abs(nodeA[1] - nodeB[1])
    return dist
