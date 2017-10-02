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
    v['alpha'] = np.mod(v['alpha'] + np.pi/180/3,2*np.pi)
    return v

def run(argv):
    #
    # Set up the parser
    #
    parser = argparse.ArgumentParser(prog="Snake.py",
                description='Play Snake on a Stackenlichten LED Display assumed to be triangles, i.e. you can move in 6 directions',
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
        slc = sl.PyMatplotSLV(30,[-30,11*30,-30,9*30])
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
    myBT = sl.AlgBackground([0.75,0.75,0.75],graph.clone())
    sample2 = sl.AlgSampleFunction(f,stepVars,vars,graph.clone())
    mAlg = sl.multAlgorithm([myBT, sample2],graph.clone())
    snake = sl.AlgSnake(39,90,5,graph.clone())
    digit1 = sl.AlgDisplayDigit(4,65,0,90,210,graph.clone())
    digit1.setParameter('Name','Tens')
    digit2 = sl.AlgDisplayDigit(2,71,0,90,210,graph.clone())
    digit2.setParameter('Name','Ones')
    sl.AlgDisplayDigit(4,68,0,90,210,graph.clone())
    seq = sl.sequentialAlgorithm([
      sl.AlgDisplayDigit(9,82,15,90,210,graph.clone()),
      sl.AlgDisplayDigit(8,82,15,90,210,graph.clone()),
      sl.AlgDisplayDigit(7,82,15,90,210,graph.clone()),
      sl.AlgDisplayDigit(6,82,15,90,210,graph.clone()),
      sl.AlgDisplayDigit(5,82,15,90,210,graph.clone()),
      sl.AlgDisplayDigit(4,82,15,90,210,graph.clone()),
      sl.AlgDisplayDigit(3,82,15,90,210,graph.clone()),
      sl.AlgDisplayDigit(2,82,15,90,210,graph.clone()),
      sl.AlgDisplayDigit(1,82,15,90,210,graph.clone()),
      sl.AlgDisplayDigit(0,82,15,90,210,graph.clone()),
      snake,
      sl.addAlgorithm([digit1,digit2],graph.clone())
    ],True,graph.clone())
    mainAlg = sl.overlayAlgorithm([mAlg,seq],[[0.0]*3]*3,graph.clone())
    alg = sl.mainAlgorithm(slc,mainAlg)

    # configure control
    c = sl.DirectionControl(alg,{"framerate":args.framerate});
    # Observers
    c.register(mainAlg)
    snake.register(digit1)
    snake.register(digit2)
    c.start()

if __name__ == "__main__":
        run(sys.argv[1:])
