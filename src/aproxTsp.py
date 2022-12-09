import networkx as nx
import numpy as np

#Aproximation algorithm with constant factor of 2opt
def twiceAroundTreeTsp(G):
    T = nx.minimum_spanning_tree(G)
    path = list(nx.dfs_preorder_nodes(T, source=0))
    pathVal = 0
    for i in range(len(path)):
        if(i == len(path) - 1):
            u = path[i]
            v = 0
            path.append(0)
            pathVal += G[u][v]['weight']
        else:
            u = path[i]
            v = path[i + 1]
            pathVal += G[u][v]['weight']
    return path, pathVal

#Aproximation algorithm with constant factor of 1.5opt
def christofidesTsp(G):

    T = nx.minimum_spanning_tree(G)
    oddNodes = []
    for node in T:
        if(T.degree[node] % 2 > 0):
            oddNodes.append(node)
    subGraph = G.subgraph(oddNodes)
    matchEdges = nx.min_weight_matching(subGraph)
    for edge in matchEdges:
        if(not T.has_edge(*edge)):
            print("Entrou!")
            T.add_edge(*edge)

    path = list(nx.dfs_preorder_nodes(T, source=0))
    pathVal = 0
    for i in range(len(path)):
        if(i == len(path) - 1):
            u = path[i]
            v = 0
            path.append(0)
            pathVal += G[u][v]['weight']
        else:
            u = path[i]
            v = path[i + 1]
            pathVal += G[u][v]['weight']
    return path, pathVal