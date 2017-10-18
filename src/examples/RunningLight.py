#!/usr/bin/env python3
import sys, argparse, os
# add parent folder in case the stackenlichten is not installed, Python will find it there
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir)
import stackenlichten as sl
import numpy as np
import includes.colormaps as cm

def run(argv):
    #
    # Set up the parser
    #
    parser = argparse.ArgumentParser(prog="Robots.py",
                description='A small test example running through the indices.',
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
    parser.add_argument('-f','--framerate', default=24.0, type=float,
                metavar='F',
                help='framerate used in the animation ')
    parser.add_argument('-n','--neighborhood', default=1, type=int,
                metavar='N',
                help="size of the neighborhood to also test the edges")
    args = parser.parse_args(argv)
    # Init Display
    if args.display == 'PyMatPlot' or args.display == 'M' or args.display == 'm':
        slc = sl.PyMatplotSLV(30,[-30,11*30,-30,9*30],{"framerate":args.framerate})
    elif args.display == 'PyTurtle' or args.display == 'T' or args.display == 't':
        slc = sl.PyTurtleSLV(30,{"framerate":args.framerate})
    elif args.display == 'PyGame' or args.display == 'G' or args.display == 'g':
        slc = sl.PyGameSLV(30,[30*x for x in [-2,10,-2,10]],
    {"framerate":args.framerate})
    else: #default
        slc = sl.FadecandySLV({"url":'localhost:7890',"framerate":args.framerate})    # Load Graph
    if len(args.graph) > 0:
        graph = sl.Graph.load(args.graph)
    else:
        raise ValueError("No graph specified")
    # Build algorithm structure
    runningLight = sl.AlgRunningLight(graph,{"Depth":args.neighborhood})
    color = sl.AlgApplyColormap(graph,{"Colormap":cm.viridis,"Type":"Gray"})
    oA = sl.overlayAlgorithm((runningLight,color),((0,0,0),(0,0,0)),graph.clone())
    alg = sl.mainAlgorithm(slc,oA)
    # configure control
    c = sl.DirectionControl(alg);
    c.start()

if __name__ == "__main__":
        run(sys.argv[1:])
