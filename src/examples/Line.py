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

class LineExample(Example):
    defaultcolor = [128,0,64]
    def __init__(this):
        super(LineExample,this).__init__("Line.py",
            "A Line.")
        # Add individual arguments
        this.vars = {'alpha':0,'scale':.5}
        this.vars2 = {'alpha':0,'scale':.25}
        this.parser.add_argument("-cr","--colorred",
        metavar="CR",default=this.defaultcolor[0],type=int,choices=range(256),
        help="Red Channel of background color")
        this.parser.add_argument("-cg","--colorgreen",
        metavar="CG",default=this.defaultcolor[1],type=int,choices=range(256),
        help="Green Channel of background color")
        this.parser.add_argument("-cb","--colorblue",
        metavar="CB",default=this.defaultcolor[2],type=int,choices=range(256),
        help="Blue Channel of background color")
        this.parser.add_argument("-s","--speed",
        metavar="S",default=30,type=int,
        help="Speed of rotation")
        this.parser.add_argument("-i","--id",
        metavar="ID",type=int,help="ID of center pixel")
    def parse_args(this,argv):
        super(LineExample,this).parse_args(argv)
        # Build algorithm structure
        bAlg = sl.AlgSampleFunction(f,stepVars,this.vars,this.graph.clone())
        bAlg2 = sl.AlgSampleFunction(f2,stepVars,this.vars,this.graph.clone())
        bAlg2 = sl.AlgBackground([
            this.args.colorred/255.0,this.args.colorgreen/255.0,this.args.colorblue/255.0
        ],
        this.graph.clone()
        )
        fAlg = sl.sequentialAlgorithm([
            sl.AlgLine(this.graph.clone(),{"ID":this.args.id,"Dir":0,"Duration":this.args.speed}),
            sl.AlgLine(this.graph.clone(),{"ID":this.args.id,"Dir":30,"Duration":this.args.speed}),
            sl.AlgLine(this.graph.clone(),{"ID":this.args.id,"Dir":60,"Duration":this.args.speed}),
            sl.AlgLine(this.graph.clone(),{"ID":this.args.id,"Dir":90,"Duration":this.args.speed}),
            sl.AlgLine(this.graph.clone(),{"ID":this.args.id,"Dir":120,"Duration":this.args.speed}),
            sl.AlgLine(this.graph.clone(),{"ID":this.args.id,"Dir":150,"Duration":this.args.speed})
        ],True,this.graph.clone())
        combAlg = sl.multAlgorithm([bAlg,fAlg],this.graph.clone(),{"FinishType":"Any"});
        addAlg = sl.overlayAlgorithm([bAlg2,combAlg],[(0,0,0),(0,0,0)],this.graph.clone())
        this.setMainAlgorithm(sl.mainAlgorithm(this.slc,addAlg))
        this.setControl(sl.SimpleControl(
            this.getMainAlgorithm(),
            parameters={'framerate':this.args.framerate}))

def run(argv):
    s = LineExample()
    s.parse_args(argv)
    s.start()

if __name__ == "__main__":
        run(sys.argv[1:])
