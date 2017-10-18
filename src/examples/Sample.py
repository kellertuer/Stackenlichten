#!/usr/bin/env python3
import sys, os
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
    v['alpha'] = np.mod(v['alpha'] + np.pi/180/5,2*np.pi)
    return v

class SampleExample(Example):
    def __init__(this):
        super(SampleExample,this).__init__("Sample.py",
            "Sample a function on the graph.")
        this.vars = {'alpha':0,'scale':.5}
    def parse_args(this,argv):
        super(SampleExample,this).parse_args(argv)
        # Build algorithm structure
        sampleAlg = sl.AlgSampleFunction(f,stepVars,this.vars,this.graph.clone())
        this.setMainAlgorithm(sl.mainAlgorithm(this.slc,sampleAlg))
        this.setControl(sl.SimpleControl(
            this.getMainAlgorithm(),
            parameters={'framerate':this.args.framerate}))

def run(argv):
    s = SampleExample()
    s.parse_args(argv)
    s.start()

if __name__ == "__main__":
        run(sys.argv[1:])
