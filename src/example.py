#!/usr/bin/env python3
import sys 
from graph import Graph
from pixel import Pixel

def run(argv):
    g = Graph("graphs/graph21.txt")
    print(g)
if __name__ == "__main__":
        run(sys.argv[1:])