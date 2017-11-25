import argparse
import stackenlichten as sl
class Example:
    """A base class for examples encapsulating the usual initializations
    common parser options and such."""
    pixelSize = 30;
    pixelFrame = [-3*30,15*30,0,13*30]
    ctrl = None
    mainAlgorithm = None
    def __init__(this,name,desc):
        """Initialize the Example, the parser, control and mainAlg.
        """
        this.parser = argparse.ArgumentParser(prog=name,
            description=desc, epilog='Stackenlichten, 2017, @kellertuer')
        # Let's add the standard options - in alphabetical order
        # B - Brightness
        this.parser.add_argument(
            "-b","--brightness",
            default=255,choices=range(256),type=int,
            metavar="B",
            help="Brightness of the display (255=default is the maximum).")
        # D - Display
        this.parser.add_argument(
            "-d","--display",
            choices=['fadecandy','f','F','PyMatPlot','m','M','PyTurtle','T','t','PyGame','G','g'],
            default='fadecandy', metavar='D',
            help='specify a vizualization: [f]adecandy for the physical Stackenlichten or one of the two availavle drawings: Py[M]atPlot or Py[T]urtle.')
        # F - frames
        this.parser.add_argument('-f','--framerate', default=24, type=int,
            metavar='F',
            help='framerate used in the animation ')
        # G Graph
        this.parser.add_argument(
            "-g", "--graph",
            metavar="G",
            default="",
            help="Specify the graph modelling the architecture of the Stackenlichten")
    def parse_args(this,argv):
        this.args = this.parser.parse_args(argv)
        # Load Graph
        if len(this.args.graph) > 0:
            this.graph = sl.Graph.load(this.args.graph)
        else:
            raise ValueError("No graph specified")
        # display
        this.DisplayParams = {
            "framerate":this.args.framerate,
            "brightness":this.args.brightness}
        if any(this.args.display == s for s in {'PyMatPlot','M','m'}):
            this.slc = sl.PyMatplotSLV(this.pixelSize,this.pixelFrame,this.DisplayParams)
        elif any(this.args.display == s for s in {'PyTurtle','T','t'}):
            this.slc = sl.PyTurtleSLV(this.pixelSize,this.DisplayParams)
        elif any(this.args.display == s for s in {'PyGame','G','g'}):
            this.slc = sl.PyGameSLV(this.pixelSize,this.pixelFrame,thiis.DisplayParams)
        else: #default
            this.slc = sl.FadecandySLV(this.DisplayParams)
    def setMainAlgorithm(this,mA):
        this.mainAlg = mA
    def getMainAlgorithm(this):
        return this.mainAlg
    def setControl(this,ct):
        this.ctrl = ct
    def getControl(this):
        return this.ctrl
    def start(this):
        this.ctrl.start()
