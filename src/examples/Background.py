#!/usr/bin/env python3
import sys, argparse, os
# add parent folder in case the stackenlichten is not installed, Python will find it there
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir)
import stackenlichten as sl
import numpy as np
import includes.colormaps as cm
from BaseExample import Example

def stepVars(vars):
    v = dict(vars)
    v['alpha'] = np.mod(v['alpha'] + np.pi/180/5,2*np.pi)
    return v

class BackgroundExample(Example):
    defaultcolor = [255,0,128]
    def __init__(this):
        super(BackgroundExample,this).__init__("Backgorund.py",
            "A simple test for plain colors")
        # Add individual arguments
        this.parser.add_argument("-cr","--colorred",
        metavar="CR",default=this.defaultcolor[0],type=int,choices=range(256),
        help="Red Channel of background color")
        this.parser.add_argument("-cg","--colorgreen",
        metavar="CG",default=this.defaultcolor[1],type=int,choices=range(256),
        help="Green Channel of background color")
        this.parser.add_argument("-cb","--colorblue",
        metavar="CB",default=this.defaultcolor[2],type=int,choices=range(256),
        help="Blue Channel of background color")
    def parse_args(this,argv):
        super(BackgroundExample,this).parse_args(argv)
        # Build algorithm structure
        backgroundAlg = sl.AlgBackground([
            this.args.colorred/255.0,
            this.args.colorgreen/255.0,
            this.args.colorblue/255.0],this.graph.clone())
        this.setMainAlgorithm(sl.mainAlgorithm(this.slc,backgroundAlg))
        this.setControl(sl.SimpleControl(
            this.getMainAlgorithm(),
            parameters={'framerate':this.args.framerate}))

def run(argv):
    s = BackgroundExample()
    s.parse_args(argv)
    s.start()

if __name__ == "__main__":
        run(sys.argv[1:])
