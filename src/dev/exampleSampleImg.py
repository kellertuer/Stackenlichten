#!/usr/bin/env python3
import sys
from graph import Graph
from pixel import Pixel
from Stackenlichten import *
from algorithm import *
from control import *
import numpy as np
import includes.colormaps as cm


def f(pts,vars):
    x = pts[0]*vars['scale']
    y = pts[1]*vars['scale']
    a = vars['alpha']
    value = (np.sin(np.cos(a)*x-np.sin(a)*y)
        + np.cos(np.sin(a)*x+np.cos(a)*y)
        + np.sin(np.cos(2*a)*x+np.sin(a)*y)
        + np.cos(-np.sin(2*a)*x+np.cos(a)*y)
        +4)/8
    return list(cm.viridis(value)[0:3])

def stepVars(vars):
    v = dict(vars)
    v['alpha'] = np.mod(v['alpha'] + np.pi/180*1,2*np.pi)
    return v


def run(argv):
    l=30
    #slc = PyMatplotSLC(l,[-3*l,9*l,0,12*l]);
    #slc = PyTurtleSLC(60);
    slc = FadecandySLC();
    #graph = Graph.load("graphs/lighthouse77.txt")
    graph = Graph.load("graphs/triangle77.txt")
    #graph = Graph.load("graphs/graph128Image.txt")
    #graph = Graph.load("graphs/graphSnail.txt")
    #graph.permute([0,21,20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1])
    vars = {'alpha':0,'scale':.5}
    sample = AlgSampleFunction(f,stepVars,vars,graph.clone())
    alg = mainAlgorithm(slc,sample)
    c = SimpleControl(alg);
    c.start()

if __name__ == "__main__":
        run(sys.argv[1:])
