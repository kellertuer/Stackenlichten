#!/usr/bin/env python3
import sys 
from graph import Graph
from pixel import Pixel
from Stackenlichten import *
from algorithm import *
from control import *

def run(argv):
    slc = FadecandySLC();
    graph = Graph.load("graphs/graph21.txt")
    algRand = AlgRandomPoints(0,0,10,graph)
    algDiff = AlgDiffusion(0.005,graph);
    algIter = metaAlgorithm([algRand,algDiff],graph)
    walk = AlgTrigWalkCycle(1,[90,330,90,210],[1,1,1,1,1,1,1,1],graph.clone())
    walk.setFramerate(5)
    mul2 = multAlgorithm([walk,algIter],graph.clone())
    alg = mainAlgorithm(slc,mul2)
    c = SimpleControl(alg);
    c.start()
    
if __name__ == "__main__":
        run(sys.argv[1:])