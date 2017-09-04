#!/usr/bin/env python3
import sys, argparse, os
# add parent folder in case the stackenlichten is not installed, Python will find it there
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
    #
    # Set up the parser
    #
    parser = argparse.ArgumentParser(prog="NorthLight.py",
                description='Put the usual pattern in viridis as a background and a lighthouse style north light on top',
                epilog='Stackenlichten, 2017, @kellertuer')
    # argument to change the display
    parser.add_argument('-d','--display',
                choices=['fadecandy','PyMatPlot','PyTurtle','PyGame'],
                default='fadecandy', metavar='D',
                help='specify a vizualization: [f]adecandy for the physical Stackenlichten or one of the two availavle drawings: Py[M]atPlot or Py[T]urtle.')
    parser.add_argument("-g", "--graph",
                metavar="G",
                default="",
                help="Specify the graph modelling the architecture of the Stackenlichten")
    parser.add_argument('-f','--framerate', default=24, type=int,
                metavar='F',
                help='framerate used in the animation ')
    args = parser.parse_args(argv)
    # variables for movement
    vars = {'alpha':0,'scale':.5}
    # Init Display
    if args.display == 'PyMatPlot' or args.display == 'M' or args.display == 'm':
        slc = sl.PyMatplotSLV(30,[-3*30,9*30,0,12*30])
    elif args.display == 'PyTurtle' or args.display == 'T' or args.display == 't':
        slc = sl.PyTurtleSLV(30)
    elif args.display == 'PyGame' or args.display == 'G' or args.display == 'g':
        slc = sl.PyGameSLV(30,[30*x for x in [-2,10,-2,10]],
        {"framerate":args.framerate})
    else: #default
        slc = sl.FadecandySLV()
    # Load Graph
    if len(args.graph) > 0:
        graph = sl.Graph.load(args.graph)
    else:
        raise ValueError("No graph specified")
    # Build algorithm structure
    point = sl.AlgRandomPoint(graph.clone(),{
            "fadein":3,
            "fadein_variance":0,
            "duration":10,
            "duration_variance":5,
            "fadeout":3,
            "fadeout_variance":0,
            "pause":9,
            "pause_variance":8,
            "repeat":True,
            "scale":args.framerate,
            "repeatrandom":True,
            "randomPositionStyle":"neighbor",
            "ID":77})
    myBT = sl.AlgBackground([0.4,0.4,0.4],graph.clone())
    sample = sl.AlgBackground([0.993248, 0.906157,0.143936],graph.clone())
    sample2 = sl.AlgSampleFunction(f,stepVars,vars,graph.clone())
    mAlg = sl.multAlgorithm([myBT, sample2],graph.clone())
    aAlg = sl.replicatePixelAlgorithm(point,77,[76,74],graph.clone())
    mAlg2 = sl.multAlgorithm([aAlg, sample],graph.clone())
    mainAlg = sl.addAlgorithm([mAlg,mAlg2],graph.clone())
    alg = sl.mainAlgorithm(slc,mainAlg)
    c = sl.SimpleControl(alg,parameters={'framerate':args.framerate});
    c.start()

if __name__ == "__main__":
        run(sys.argv[1:])
