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
    v['alpha'] = np.mod(v['alpha'] + np.pi/180*1.5,2*np.pi)
    return v


def run(argv):
    slc = FadecandySLC();
    graph = Graph.load("graphs/graph21.txt")
    vars = {'alpha':0,'scale':.5}
    sample = AlgSampleFunction(f,stepVars,vars,graph.clone())
    walk = AlgTrigWalkCycle(1,[90,330,90,210],[1,1,1,1,1,1,1,1],graph.clone())
    walk.setFramerate(1)
    add1 = addAlgorithm([
        AlgBackground([0,0,0],graph.clone()),
        walk],graph.clone())
    mul2 = multAlgorithm([sample,add1],graph.clone())
    alg = mainAlgorithm(slc,mul2)
    c = SimpleControl(alg);
    c.start()
    
if __name__ == "__main__":
        run(sys.argv[1:])