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
        this.parser.add_argument("-sb",'--samplebackground',action="store_true",default=False,help="Sample a function (true) or take a color as background (false, default).")
        this.parser.add_argument("-sf",'--sampleforeground',action="store_true",default=False,help="Sample a function (true) or take a color (white - [CR,CG,.CB], default).")
        this.parser.add_argument("-s","--speed",
        metavar="S",default=30,type=int,
        help="Speed of rotation")
        this.parser.add_argument("-i","--id",
        metavar="ID",type=int,help="ID of center pixel")
    def parse_args(this,argv):
        super(LineExample,this).parse_args(argv)
        r = this.args.colorred
        g = this.args.colorgreen
        b = this.args.colorblue
        # Build algorithm structure
        if this.args.sampleforeground:
            bAlg = sl.AlgSampleFunction(f,stepVars,this.vars,this.graph.clone())
        else:
            if r==255 and g==255 and b==255: # hack
                c = [0.001,0.001,0.001]
            else:
                c = [1.0-r/255.0,1.0-g/255.0,1.0-b/255.0]
            bAlg = sl.AlgBackground(c,this.graph.clone())
        if this.args.samplebackground:
            bAlg2 = sl.AlgSampleFunction(f2,stepVars,this.vars,this.graph.clone())
        else:
            bAlg2 = sl.AlgBackground([r/255.0,g/255.0,b/255.0],
                this.graph.clone())
        l1 = sl.AlgLine(this.graph.clone(),{"ID":this.args.id,"Dir":0,"Duration":this.args.speed})
        l2 = sl.AlgLine(this.graph.clone(),{"ID":this.args.id,"Dir":30,"Duration":this.args.speed})
        l3 =    sl.AlgLine(this.graph.clone(),{"ID":this.args.id,"Dir":60,"Duration":this.args.speed})
        l4 =     sl.AlgLine(this.graph.clone(),{"ID":this.args.id,"Dir":90,"Duration":this.args.speed})
        l5 = sl.AlgLine(this.graph.clone(),{"ID":this.args.id,"Dir":120,"Duration":this.args.speed})
        l6 = sl.AlgLine(this.graph.clone(),{"ID":this.args.id,"Dir":150,"Duration":this.args.speed})
        fAlg = sl.sequentialAlgorithm([l1,l2,l3,l4,l5,l6],True,this.graph.clone())
        combAlg = sl.multAlgorithm([bAlg,fAlg],this.graph.clone(),{"FinishType":"Any"});  addAlg = sl.overlayAlgorithm([bAlg2,combAlg],[(0,0,0),(0,0,0)],this.graph.clone())
        this.setMainAlgorithm(sl.mainAlgorithm(this.slc,addAlg))
        this.setControl(sl.DirectionControl(
            this.getMainAlgorithm(),
            parameters={'framerate':this.args.framerate}))
        this.getControl().register(l1)
        this.getControl().register(l2)
        this.getControl().register(l3)
        this.getControl().register(l4)
        this.getControl().register(l5)
        this.getControl().register(l6)

def run(argv):
    s = LineExample()
    s.parse_args(argv)
    s.start()

if __name__ == "__main__":
        run(sys.argv[1:])
