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

class NorthLightExample(Example):
    def __init__(this):
        super(NorthLightExample,this).__init__("NorthLight.py",
            "Put the usual pattern in viridis as a background and a lighthouse style north light on top")
        this.vars = {'alpha':0,'scale':.5}
    def parse_args(this,argv):
        super(NorthLightExample,this).parse_args(argv)
        # Build algorithm structure
        point = sl.AlgRandomPoint(this.graph.clone(),{
            "fadein":3, "fadein_variance":0,
            "duration":10, "duration_variance":5,
            "fadeout":3, "fadeout_variance":0,
            "pause":9, "pause_variance":8,
            "repeat":True, "scale":this.args.framerate,
            "repeatrandom":True,
            "randomPositionStyle":"neighbor",
            "ID":100})
        myBT = sl.AlgBackground([0.3,0.3,0.3],this.graph.clone())
        sample = sl.AlgBackground([0.993248, 0.906157,0.143936],this.graph.clone())
        sample2 = sl.AlgSampleFunction(f,stepVars,this.vars,this.graph.clone())
        mAlg = sl.multAlgorithm([myBT, sample2],this.graph.clone())
        aAlg = sl.replicatePixelAlgorithm(point,100,[97,98,99],this.graph.clone())
        mAlg2 = sl.multAlgorithm([aAlg, sample],this.graph.clone())
        northLightAlg = sl.addAlgorithm([mAlg,mAlg2],this.graph.clone())
        this.setMainAlgorithm(sl.mainAlgorithm(this.slc,northLightAlg))
        this.setControl(sl.SimpleControl(
            this.getMainAlgorithm(),
            parameters={'framerate':this.args.framerate}))

def run(argv):
    s = NorthLightExample()
    s.parse_args(argv)
    s.start()

if __name__ == "__main__":
        run(sys.argv[1:])
