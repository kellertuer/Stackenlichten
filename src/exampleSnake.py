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

def f2(pts,vars):
    x = pts[0]*vars['scale']
    y = pts[1]*vars['scale']
    a = -2*vars['alpha']
    value = (np.sin(np.cos(a)*x-np.sin(a)*y)
        + np.cos(np.sin(a)*x+np.cos(a)*y)
        + np.sin(np.cos(2*a)*x+np.sin(a)*y)
        + np.cos(-np.sin(2*a)*x+np.cos(a)*y)
        +4)/8
    return list(cm.magma(value)[0:3])

def stepVars(vars):
    v = dict(vars)
    v['alpha'] = np.mod(v['alpha'] + np.pi/180*1,2*np.pi)
    return v


def run(argv):
    l=30
    vars = {'alpha':0,'scale':.5}
    #slc = PyMatplotSLC(l,[-3*l,9*l,0,12*l]);
    slc = FadecandySLC();
    graph = Graph.load("graphs/triangle77.txt")
    #vars = {'alpha':0,'scale':.5}
    #sample = AlgSampleFunction(f,stepVars,vars,graph.clone())
    running = AlgTrigWalkCycle(28,[90,330,210,90,330,210,90,330,210,90,330,210,90,330,210,240],[28]*5,[1,1,3,3,3,5,5,5,7,7,7,9,9,9,9,1],graph.clone())
    sample = AlgSampleFunction(f,stepVars,vars,graph.clone())
    mAlg = multAlgorithm([running,sample],graph.clone())
    sample2 = AlgSampleFunction(f2,stepVars,vars,graph.clone())
    mG = graph.clone()
    randomAlg = AlgRandomBlink(3,True,15,4,graph.clone())
    myBT = AlgBackground([0.33,0.33,0.33],graph.clone())
    background = overlayAlgorithm([myBT,randomAlg],[[0.0,0.0,0.0]]*3,graph.clone())
    mAlg2 = multAlgorithm([background, sample2],graph.clone())
    metaAlg = overlayAlgorithm([mAlg2,mAlg],[[0.0,0.0,0.0]]*3,graph.clone())
    alg = mainAlgorithm(slc,metaAlg)
    #alg = mainAlgorithm(slc,mAlg2)
    c = DirectionControl(alg);
    c.start()
    
if __name__ == "__main__":
        run(sys.argv[1:])