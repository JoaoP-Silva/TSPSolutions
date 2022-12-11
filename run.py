import os
import sys
import networkx as nx
import tracemalloc

ROOT = os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir))
sys.path.append(("%s/src")%(ROOT))

from genInput import genTspInput
from bnbTsp import bnbTSP
from aproxTsp import *
import time

def writeGraph(G, size, seed, model):
    f = open(("%s/experiments/graphSize_%d_%s_%d.txt")%(ROOT, size, model, seed), 'w')
    weight = nx.get_edge_attributes(G,'weight')
    for edge in G.edges():
      data = "(%d, %d);%d\n" % (edge[0], edge[1], weight[(edge[0], edge[1])])
      f.write(data)
    f.close()

def writePath(path, pathLen,size, algorithm, seed, model):
    f = open(("%s/experiments/path_at_graphSize_%d_%s_%d.txt")%(ROOT, size, model, seed), 'a')
    data = "Path = %s, Path size = %f, Using algorithm = %d\n"%(path, pathLen, algorithm)
    f.write(data)
    f.close()

#Write a csv file with metrics on dir results
def writeMetics(metrics):

    algorithm = metrics[0]
    i = metrics[1]
    path_len = metrics[2]
    time =  metrics[3]
    curr_mem = metrics[4]
    peak_mem = metrics[5]
    distance_funct = metrics[6]
    seed = metrics[7]

    isExist = os.path.exists(("%s/results/result_%s_%d.csv")%(ROOT, model, seed))
    if(not isExist):
        f = open(("%s/results/result_%s_%d.csv")%(ROOT, model, seed), 'w')
        f.write("algorithm, i, path_len, time, curr_mem, peak_mem, distance_funct, seed\n")
    else:
        f = open(("%s/results/result_%s_%d.csv")%(ROOT, model, seed), 'a')

    data = (("%d, %d, %f, %f, %f, %f, %s, %d\n") % 
            (algorithm, i, path_len, time, curr_mem, peak_mem, distance_funct, seed))
    f.write(data)
    f.close
        

# Input model: python run.py < algorithm > < i > < seed > < function >
# <algorithm> can be "bnb" to use branch and bound algorithm to solve TSP
# instance ou "aprox" to solve the TSP using the algorithms Twice around the tree
# and Christofides.
# <i> is an integer according to the experiment input size 2^i.
# <seed> is an integer to be the random seed.
# <function> can be "man" (for manhattan distance)
# or "euc" (for euclidean distance).
#
#
# On output branch and bound is algorithm 0, twice around the tree is 1
# and Christofides is 2
if __name__ == '__main__':

    
    if(len(sys.argv) < 5):
        print("Too few arguments for run.py")
    
    elif(len(sys.argv) > 5):
        print("Too many arguments for run.py")

    algorithm = str(sys.argv[1])
    i = int(sys.argv[2])
    seed = int(sys.argv[3])
    model = str(sys.argv[4])

    

    if(i <= 0):
        print("i must be greater than 0")

    elif(seed < 0):
        print("seed must be at least 0")
    
    elif(model != "euc" and model != "man"):
        print("Unknown model")
    
    elif(algorithm != "aprox" and algorithm != "bnb"):
        print("Unknown algorithm")
    else:
        size = 2**i
        euclideanG, manhattanG = genTspInput(size, seed)
        if(algorithm == "bnb"):
            if(model == "euc"):
                writeGraph(euclideanG, i, seed, "euc")
                start_time = time.time()
                tracemalloc.start()
                path, pathLen = bnbTSP(euclideanG)
                alg = 0
                current, peak = tracemalloc.get_traced_memory()
                execTime = time.time() - start_time
                metrics = [alg, i, pathLen, execTime, current, peak, "euc", seed]
                writeMetics(metrics)
                writePath(path, pathLen,i, alg, seed, "euc")
            
            elif(model == "man"):
                writeGraph(manhattanG, i, seed, "man")
                start_time = time.time()
                tracemalloc.start()
                path, pathLen = bnbTSP(manhattanG)
                alg = 0
                current, peak = tracemalloc.get_traced_memory()
                execTime = time.time() - start_time
                metrics = [alg, i, pathLen, execTime, current, peak, "man", seed]
                writeMetics(metrics)
                writePath(path, pathLen,i, alg, seed, "man")

        else:
            if(model == "euc"):
                writeGraph(euclideanG, i, seed, "euc")
                start_time = time.time()
                tracemalloc.start()
                path, pathLen = twiceAroundTreeTsp(euclideanG)
                alg = 1
                current, peak = tracemalloc.get_traced_memory()
                execTime = time.time() - start_time
                metrics = [alg, i, pathLen, execTime, current, peak, "euc", seed]
                writeMetics(metrics)
                writePath(path, pathLen,i, alg, seed, "euc")

                tracemalloc.clear_traces()
                start_time = time.time()
                path, pathLen = christofidesTsp(euclideanG)
                alg = 2
                current, peak = tracemalloc.get_traced_memory()
                execTime = time.time() - start_time
                metrics = [alg, i, pathLen, execTime, current, peak, "euc", seed]
                writeMetics(metrics)
                writePath(path, pathLen,i, alg, seed, "euc")
            
            elif(model == "man"):
                writeGraph(manhattanG, i, seed, "man")
                start_time = time.time()
                tracemalloc.start()
                path, pathLen = twiceAroundTreeTsp(manhattanG)
                alg = 1
                current, peak = tracemalloc.get_traced_memory()
                execTime = time.time() - start_time
                metrics = [alg, i, pathLen, execTime, current, peak, "man", seed]
                writeMetics(metrics)
                writePath(path, pathLen,i, alg, seed, "man")

                tracemalloc.clear_traces()
                start_time = time.time()
                tracemalloc.start()
                path, pathLen = christofidesTsp(manhattanG)
                alg = 2
                current, peak = tracemalloc.get_traced_memory()
                execTime = time.time() - start_time
                metrics = [alg, i, pathLen, execTime, current, peak, "man", seed]
                writeMetics(metrics)
                writePath(path, pathLen,i, alg, seed, "man")