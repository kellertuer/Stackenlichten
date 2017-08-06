#!/usr/bin/env python3
import sys
# add parent folder in case the stackenlichten is not installed, Python will find it there
import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir)
import stackenlichten as sl
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
    v['alpha'] = np.mod(v['alpha'] + np.pi/180/5,2*np.pi)
    return v

def run(argv):
    l=30
    vars = {'alpha':0,'scale':.5}
    slc = sl.PyMatplotSLV(l,[-3*l,9*l,0,12*l]);
    #slc = FadecandySLV();
    graph = sl.Graph.load("graphs/triangle77.txt")
    #vars = {'alpha':0,'scale':.5}
    #sample = AlgSampleFunction(f,stepVars,vars,graph.clone())
    myBT = sl.AlgBackground([0.75,0.75,0.75],graph.clone())
    sample2 = sl.AlgSampleFunction(f2,stepVars,vars,graph.clone())
    mAlg = sl.multAlgorithm([myBT, sample2],graph.clone())
    snake = sl.AlgSnake(28,90,5,graph.clone())
    seq = sl.sequentialAlgorithm([
      sl.AlgDisplayDigit(9,55,15,90,210,graph.clone()),
      sl.AlgDisplayDigit(8,55,15,90,210,graph.clone()),
      sl.AlgDisplayDigit(7,55,15,90,210,graph.clone()),
      sl.AlgDisplayDigit(6,55,15,90,210,graph.clone()),
      sl.AlgDisplayDigit(5,55,15,90,210,graph.clone()),
      sl.AlgDisplayDigit(4,55,15,90,210,graph.clone()),
      sl.AlgDisplayDigit(3,55,15,90,210,graph.clone()),
      sl.AlgDisplayDigit(2,55,15,90,210,graph.clone()),
      sl.AlgDisplayDigit(1,55,15,90,210,graph.clone()),
      sl.AlgDisplayDigit(0,55,15,90,210,graph.clone()),
      snake,
      sl.addAlgorithm([
        sl.AlgDisplayDigit(4,68,0,90,210,graph.clone()),
        sl.AlgDisplayDigit(2,59,0,90,210,graph.clone())],graph.clone())
    ],True,graph.clone(),{"PassValue":[ {"From":10,"FromKey":"GameScore","To":[[11,0],[11,1]],"ToKey":"Digit","Type":"SplitDigits"} ]})
    mainAlg = sl.overlayAlgorithm([mAlg,seq],[[0.0]*3]*3,graph.clone())
    alg = sl.mainAlgorithm(slc,mainAlg)
    c = sl.DirectionControl(alg);
    c.start()

if __name__ == "__main__":
        run(sys.argv[1:])
