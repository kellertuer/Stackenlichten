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
                description='A small turn-based game, where you have to escape robots! You can move one step each round using erfvcd.',
                epilog='Stackenlichten, 2017, @kellertuer')
    # argument to change the display
    parser.add_argument('-d','--display',
                choices=['fadecandy','PyMatPlot','PyTurtle'],
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
        slc = sl.FadecandySLV()    # Load Graph
    if len(args.graph) > 0:
        graph = sl.Graph.load(args.graph)
    else:
        raise ValueError("No graph specified")
    # Build algorithm structure
    walker = sl.AlgWalker(28,graph.clone())
    robot1 = sl.AlgBasicRobot(55,walker,graph.clone())
    robot2 = sl.AlgBasicRobot(77,walker,graph.clone())
    robot3 = sl.AlgBasicRobot(30,walker,graph.clone())
    robot4 = sl.AlgBasicRobot(40,walker,graph.clone())
    robotGroup = sl.addAlgorithm([robot1,robot2,robot3,robot4,walker],graph.clone(),{"FinishType":"Any"})
    digit1 = sl.AlgDisplayDigit(4,68,0,90,210,graph.clone())
    digit1.setParameter('Name','Tens')
    digit2 = sl.AlgDisplayDigit(2,59,0,90,210,graph.clone())
    digit2.setParameter('Name','Ones')
    seqAlg = sl.sequentialAlgorithm([
          robotGroup,
          sl.addAlgorithm([digit1,digit2],graph.clone())
        ],True,graph.clone())
    alg = sl.mainAlgorithm(slc,seqAlg)

    # configure control
    c = sl.DirectionControl(alg,{"framerate":args.framerate});
    # Observers
    c.register(walker)
    c.register(digit1)
    c.register(digit2)
    walker.register(digit1)
    walker.register(digit2)
    c.start()

if __name__ == "__main__":
        run(sys.argv[1:])
