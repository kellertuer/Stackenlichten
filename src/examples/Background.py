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
    parser = argparse.ArgumentParser(prog="Background.py",
                description='Simple Test backgroundns',
                epilog='Stackenlichten, 2017, @kellertuer')
    # argument to change the display
    parser.add_argument('-d','--display',
                choices=['fadecandy','f','F','PyMatPlot','m','M','PyTurtle','T','t','PyGame','G','g'],
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
        slc = sl.PyMatplotSLV(30,[-3*30,15*30,0,13*30])
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
    myBT = sl.AlgBackground([1,.3,.3],graph.clone())
    # myBT = sl.AlgSampleFunction(f,stepVars,vars,graph.clone())
    alg = sl.mainAlgorithm(slc,myBT)

    # configure control
    c = sl.SimpleControl(alg,{"framerate":args.framerate});
    c.start()

if __name__ == "__main__":
        run(sys.argv[1:])
