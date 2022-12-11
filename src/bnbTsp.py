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

 #Solve TSP using branch and bound technique. Return the solution (list of nodes)
 #and a the path lenght (float value)
def bnbTSP(graph):
    initialEstimate = initialBound(graph)
    level = 2
    visited = set()
    visited.add(0)
    path = [0]
    queue = []
    for neighbor in graph[0]:
        visitedCpy = visited.copy()
        visitedCpy.add(neighbor)
        pathCpy = path.copy()
        pathCpy.append(neighbor)
        currPathVal = graph[0][neighbor]['weight']
        val = bound(pathCpy, initialEstimate, graph)
        newBnbNode = bnbNode(val, level, visitedCpy, pathCpy, currPathVal)
        heapq.heappush(queue, newBnbNode)   

    best = math.inf
    sol = []
    n = graph.number_of_nodes()
    while(len(queue) > 0):
        thisNode = heapq.heappop(queue)
        lastNode = thisNode.sol[-1]
        if(thisNode.cost < best):
            if (thisNode.level < n):
                for neighbor in graph[lastNode]:
                    if(neighbor not in thisNode.visited):
                        visitedCpy = thisNode.visited.copy()
                        visitedCpy.add(neighbor)
                        pathCpy = thisNode.sol.copy()
                        pathCpy.append(neighbor)
                        currPathVal = thisNode.solVal
                        currPathVal += graph[lastNode][neighbor]['weight']
                        thisLevel = thisNode.level + 1
                        val = bound(pathCpy, initialEstimate, graph)
                        if(val < best):
                            newBnbNode = bnbNode(val, thisLevel, visitedCpy, pathCpy, currPathVal)
                            heapq.heappush(queue, newBnbNode)

            else:
                pathCpy = thisNode.sol
                pathCpy.append(0)
                currPathVal = thisNode.solVal
                currPathVal += graph[lastNode][0]['weight']
                val = currPathVal
                if(val < best):
                    best = val
                    sol = pathCpy

    return sol, best






def bound(currPath, initialEstimate, G):

    estimate = np.copy(initialEstimate)
    for i in range(len(currPath) - 1):
        #Sum the other edge from last added node
        u = currPath[i]
        v = currPath[i + 1]
        edgeVal = G[u][v]['weight']
        if(edgeVal != initialEstimate[u][0]):
            estimate[u][1] = edgeVal
        if(edgeVal != initialEstimate[v][0]):
            estimate[v][1] = edgeVal
        
    val = 0
    #Sum all selected edges from other nodes
    val = np.sum(estimate)
    
    return math.ceil(val/2)

#Returns the initialEstimate matrix
def initialBound(G):
    i = 0
    initialEstimate = np.zeros((G.number_of_nodes(), 2))
    for node in G:
        edges = []
        for neighbor in G[node]:
            edges.append(G[node][neighbor]['weight'])
        twoSmallest = heapq.nsmallest(2, edges)
        initialEstimate[i][0] = twoSmallest[0]
        initialEstimate[i][1] = twoSmallest[1]
        i += 1

    return initialEstimate
