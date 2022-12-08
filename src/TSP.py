import networkx as nx
import numpy as np
import heapq
import math


class bnbNode:
    def __init__(self, cost, level, visited, sol, solVal):
        self.cost = cost
        self.level = level
        self.sol = sol
        self.visited = visited
        self.solVal = solVal
    
    def __gt__(self, other):
        if(self.cost > other.cost):
            return True
        elif(self.cost == other.cost):
            if(self.level > other.level):
                return True
    
    def __hash__(self):
        return hash(self.visited)

    
def bnbTSP(graph, output):
    initVal, initialEstimate = initialBound(graph)
    level = 1
    visited = set()
    visited.add(0)
    path = [0]
    queue = []
    for neighbor in graph[0]:
        visitedCpy = visited
        visitedCpy.add(neighbor)
        pathCpy = path
        pathCpy.append(neighbor)
        currPathVal = graph[0][neighbor]['weight']
        val = bound(visitedCpy, pathCpy, currPathVal, initialEstimate, graph)
        newBnbNode = bnbNode(val, level, visitedCpy, pathCpy, currPathVal)
        heapq.heappush(queue, newBnbNode)   

    best = math.inf
    sol = []
    n = graph.number_of_nodes()
    while(len(queue) > 0):
        thisNode = heapq.heappop(queue)
        lastNode = thisNode.sol[-1]
        if(thisNode.level > n):
            if thisNode.cost < best:
                best = thisNode.cost
                sol = thisNode.sol
        elif(thisNode.cost < best):
            if thisNode.level < n:
                for neighbor in graph[lastNode]:
                    if(neighbor not in thisNode.visited):
                        visitedCpy = thisNode.visited
                        visitedCpy.add(neighbor)
                        pathCpy = thisNode.sol
                        pathCpy.append(neighbor)
                        currPathVal = thisNode.solVal
                        currPathVal += graph[lastNode][neighbor]['weight']
                        thisLevel = thisNode.level + 1
                        val = bound(visitedCpy, pathCpy, currPathVal, initialEstimate, graph)
                        if(val < best):
                            newBnbNode = bnbNode(val, thisLevel, visitedCpy, pathCpy, currPathVal)
                            heapq.heappush(queue, newBnbNode)
            else:
                pathCpy = thisNode.sol
                pathCpy.append(0)
                currPathVal = thisNode.solVal
                currPathVal += graph[lastNode][0]['weight']
                val = bound(thisNode.visited, pathCpy, currPathVal, initialEstimate, graph)
                if(val < best):
                    newBnbNode = bnbNode(val, thisNode.level + 1, thisNode.visited, pathCpy, currPathVal)

    return sol, best






def bound(visitedNodes, currPath, currPathVal, initialEstimate, G):

    #Consider the value of current path
    val = currPathVal

    #Sum the other edge from last added node
    u = currPath[-1]
    v = currPath[-2]
    edgeVal = G[u][v]['weight']
    if(edgeVal != initialEstimate[u][1]):
        val += initialEstimate[u][0]
    else:
        val += initialEstimate[u][1]
    
    #Sum all selected edges from other nodes
    for node in G:
        if(node not in visitedNodes):
            for i in range(0, 2):
                val += initialEstimate[node][i]
    
    return val

#Returns the initialEstimate matrix and a value
def initialBound(G):
    i = 0
    val = 0
    initialEstimate = mat = [[0 for _ in range(2)] for _ in range(G.number_of_nodes())]
    for node in G:
        edges = []
        for neighbor in G[node]:
            edges.append(G[node][neighbor]['weight'])
        twoSmallest = heapq.nsmallest(2, edges)
        val += twoSmallest[0] + twoSmallest[1]
        initialEstimate[i][0] = twoSmallest[0]
        initialEstimate[i][1] = twoSmallest[1]
        i += 1

    return val, initialEstimate
