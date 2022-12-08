import os
import sys


ROOT = os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir))
sys.path.append(("%s/src")%(ROOT))

from genInput import * 

if __name__ == '__main__':

    seed = -1
    print("\t- - - Experiment menu - - -")
    while(seed < 0):
        print("\nEnter a integer number i >= 0 to be the random seed")
        seed = int(input())
    
    btn = -1
    while(btn < 0):
        print("Select the input size:")
        print("\t 1 - Select a custom i to run one experiment with an instance of size 2^i")
        print("\t 2 - Run 7 experiments with the input size ranging from 2^4 to 2^10")
        print("\n\t 0 - QUIT")
        btn = int(input())
        if(btn >= 0):
            break
    
    if(btn == 1):
        i = 1
        while(i <= 1):
            print("Enter the value of i > 1 to define the input size 2^i")
            i = int(input())
        size = 2**i
        genTspInput(size, seed)

    elif(btn == 2):
        for i in range(4, 11):
            size = 2**i
            genTspInput(size, seed)
    