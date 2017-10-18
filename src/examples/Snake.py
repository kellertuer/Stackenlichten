#!/usr/bin/env python3
import sys, argparse, os
# add parent folder in case the stackenlichten is not installed, Python will find it there
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir)
import stackenlichten as sl
import numpy as np
import includes.colormaps as cm
from BaseExample import Example
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
    v['alpha'] = np.mod(v['alpha'] + np.pi/180/3,2*np.pi)
    return v

class SnakeExample(Example):
    def __init__(this):
            super(SampleExample,this).__init__("Snake.py",
                "Play Snake on a Stackenlichten LED Display assumed to be triangles, i.e. you can move in 6 directions.Keys:\n f,r,e,d,x,c: 6 directions\nk,l : turn left/right.")
            this.vars = {'alpha':0,'scale':.5}
        def parse_args(this,argv):
            super(SnakeExample,this).parse_args(argv)
            # Build algorithm structure
                myBT = sl.AlgBackground([0.75,0.75,0.75],this.graph.clone())
                sample2 = sl.AlgSampleFunction(f,stepVars,vars,this.graph.clone())
                mAlg = sl.multAlgorithm([myBT, sample2],this.graph.clone())
                snake = sl.AlgSnake(39,90,5,this.graph.clone())
                digit1 = sl.AlgDisplayDigit(4,65,0,90,210,this.graph.clone())
                digit1.setParameter('Name','Tens')
                digit2 = sl.AlgDisplayDigit(2,71,0,90,210,this.graph.clone())
                digit2.setParameter('Name','Ones')
                sl.AlgDisplayDigit(4,68,0,90,210,this.graph.clone())
                seq = sl.sequentialAlgorithm([
                  sl.AlgDisplayDigit(9,82,15,90,210,this.graph.clone()),
                  sl.AlgDisplayDigit(8,82,15,90,210,this.graph.clone()),
                  sl.AlgDisplayDigit(7,82,15,90,210,this.graph.clone()),
                  sl.AlgDisplayDigit(6,82,15,90,210,this.graph.clone()),
                  sl.AlgDisplayDigit(5,82,15,90,210,this.graph.clone()),
                  sl.AlgDisplayDigit(4,82,15,90,210,this.graph.clone()),
                  sl.AlgDisplayDigit(3,82,15,90,210,this.graph.clone()),
                  sl.AlgDisplayDigit(2,82,15,90,210,this.graph.clone()),
                  sl.AlgDisplayDigit(1,82,15,90,210,this.graph.clone()),
                  sl.AlgDisplayDigit(0,82,15,90,210,this.graph.clone()),
                  snake,
                  sl.addAlgorithm([digit1,digit2],this.graph.clone())
                ],True,this.graph.clone())
                snakeAlg = sl.overlayAlgorithm([mAlg,seq],[[0.0]*3]*3,this.graph.clone())
                this.setMainAlgorithm(sl.mainAlgorithm(this.slc,snakeAlg))
                this.setControl(sl.DirectionControl(this.getMainAlgorithm(),
                parameters={'framerate':this.args.framerate}))
                this.getControl().register(snakeAlg)


def run(argv):
    c = sl.DirectionControl(alg);
    # Observers
    c.register(mainAlg)
    snake.register(digit1)
    snake.register(digit2)
    c.start()

if __name__ == "__main__":
        run(sys.argv[1:])
