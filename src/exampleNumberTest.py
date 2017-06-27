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
    v['alpha'] = np.mod(v['alpha'] + np.pi/180/5,2*np.pi)
    return v


def run(argv):
    l=30
    vars = {'alpha':0,'scale':.5}
    #slc = PyMatplotSLC(l,[-3*l,9*l,0,12*l]);
    slc = FadecandySLC();
    graph = Graph.load("graphs/triangle77.txt")
    #vars = {'alpha':0,'scale':.5}
    #sample = AlgSampleFunction(f,stepVars,vars,graph.clone())
    myBT = AlgBackground([0.75,0.75,0.75],graph.clone())
    sample2 = AlgSampleFunction(f2,stepVars,vars,graph.clone())
    mAlg = multAlgorithm([myBT, sample2],graph.clone())
    snake = AlgSnake(28,90,5,graph.clone())
    mainAlg = overlayAlgorithm([mAlg,snake],[[0.0,0.0,0.0]]*3,graph.clone())
    seq = sequentialAlgorithm([
      addAlgorithm([AlgDisplayDigit(1,68,15,90,210,graph.clone()),AlgDisplayDigit(0,59,15,90,210,graph.clone())],graph.clone()),
      AlgDisplayDigit(9,59,15,90,210,graph.clone()),
      AlgDisplayDigit(8,59,15,90,210,graph.clone()),
      AlgDisplayDigit(7,59,15,90,210,graph.clone()),
      AlgDisplayDigit(6,59,15,90,210,graph.clone()),
      AlgDisplayDigit(5,59,15,90,210,graph.clone()),
      AlgDisplayDigit(4,59,15,90,210,graph.clone()),
      AlgDisplayDigit(3,59,15,90,210,graph.clone()),
      AlgDisplayDigit(2,59,15,90,210,graph.clone()),
      AlgDisplayDigit(1,59,15,90,210,graph.clone()),
      AlgDisplayDigit(0,59,15,90,210,graph.clone()),
      mainAlg
    ],False,graph.clone())
    alg = mainAlgorithm(slc,seq)
    c = DirectionControl(alg);
    c.start()
    
if __name__ == "__main__":
        run(sys.argv[1:])