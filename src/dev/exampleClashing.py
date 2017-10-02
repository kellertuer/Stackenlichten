#!/usr/bin/env python3
import sys
from graph import Graph
from Pixel import Pixel
from Stackenlichten import *
from algorithm import *
from control import *

def run(argv):
    # slc = PyMatplotSLC(l,[-3*l,9*l,0,12*l]);
    slc = FadecandySLC();
    graph = Graph.load("graphs/graph21.txt")
    malg = multAlgorithm([
        AlgBackground([0.75,0.5625,.0],graph.clone()),
        AlgTrigWalkCycle(1,[90,330,90,210],[1,1,1,1,1],graph.clone())
        ],graph.clone())
    malg2 = multAlgorithm([
        AlgBackground([0.1875,.0,0.75],graph.clone()),
        AlgTrigWalkCycle(19,[150,270,30,270],[1,1,1,1,1],graph.clone())
        ],graph.clone())
    aAlg = addAlgorithm([AlgBackground([0,0.2,0],graph.clone()),malg,malg2],graph)
    alg = mainAlgorithm(slc,aAlg)
    c = SimpleControl(alg);
    c.start()

if __name__ == "__main__":
        run(sys.argv[1:])
