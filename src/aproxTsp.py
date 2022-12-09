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

