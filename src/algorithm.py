from graph import Graph
import numpy as np

def abstractmethod(method):
    def default_abstract_method(*args, **kwargs):
        raise NotImplementedError('call to abstract method ' + repr(method))

    default_abstract_method.__name__ = method.__name__
    
    return default_abstract_method

class Algorithm(Graph):
    """
    All algorithm serves as decorator for a graph, such that any algorthm may
    keep a list of sub algorithms to be performed within the algorithm
    """"
    
    this.osf = 1
    
    def __init(this,fn="",graph=None):
        "Initialize the algorithm to act on a certain graph object"
        this.super(AlgTrigWalk,this).__init__("",graph);
    
    @abstractmethod
    def step(this): pass
        "perform a step/frame of the algorithm"

    @abstractmethod
    def getFramerate(this):
        "perform a step only each kth step of the parent algorithm or framerate if this is a main algorithm"
        return this.osf;

    def setFramerate(this,osf):
        "perform a step only each kth step of the parent algorithm"
        this.osf=osf;
        
    @abstractmethod
    def isFinished(this): pass
        "returns whether this algorithm has finished running"

    @abstractmethod
    def step(this): pass
        "perform a step of the algorithm"

    @abstractmethod
    def getFollowUp(this): pass
        "if the algorithm is finished it may provide a followUpAlgorithm or set of Algorithms"

class metaAlgorithm(Algorithm):
    """
    A meta algorithm consists of a set of algorithms that are iterated in each
    step and deleted is finsihed
    """
    def __init(algorithms,fn="",graph=None):
        super(metaAlgorithm,this).__init__(fn,graph);
        this.algorithms = algorithms;
        this.iter = 0;
    
    def step(this):
        if len(this.algorithms) > 0:
            this.iter = this.iter + 1;
            # TODO: check if finished ones have a followUp?
            #remove finished
            this.algorithms = [x for x in this.algorithms if not x.isFinished]
            if len(this.algorithms) > 0:
                # step remaining ones
                for x in this.algorithms
                    if (iter%x.getFramerate())==0
                        x.step()
    
    def isFinished(this):
        return len(this.algorithms)==0

class mainAlgorithm(metaAlgorithm):
    """
    The main Algorithms class connects the graph with the view, a Stackenlichten
    and updates the piel after each step, which consists of running all its child algorithms
    """
    def __init__(SLC,algorithms,fn="",graph=None):
        super(mainAlgorithm,this).__init__(algorithms,fn,graph)
        this.SLC = SLC
    
    def step(this):
        super(mainAlgorithm,this).step()
        # put pixels to leds
        this.SLC.render(this)
        
        
        
class AlgTrigWalkCycle(Algorithm):
    """
    The algorithm to run in circles on the trig grid. Following a direction
    until the border and continuing with the next direction; cycling through these.
    """
    def __init__(this,startID,directions,trailNum,fn="",graph=None):
        this.super(AlgTrigWalk,this).__init__(fn,graph);
        this.startID=startID
        this.directions=directions
        this.actDir = 0
        this.currID = startID
        this.currAlg = AlgTrigWalk(graph,startID,directions[this.actDir],trailNum)
        this.trailNum = trailNum
    
    def step(this):
        if this.currAlg.isFinished(): #start next one
            this.actDir = (this.actDir+1)%(len(this.directions))
            curPos = this.currAlg.getactualPosition();
            this.currAlg = AlgTrigWalk(curPos,this.directions[this.actDir],this.trailNum,"",this.currAlg)
        else:
            this.currAlg.step()
    
    def isFinished(): #infinite loop
        return false

class AlgTrigWalk(Algorithm):
    """
    An algorithm running along a direction starting from a pixel with a tail in
    a colormap
    """
    
    AVAILABLE_DIRECTIONS = [0,30,60,90,120,150,180,210,240,270,300,330]
    # we have to alternate, these are for /\ triangles, for \/ start with the second in dex
    __INNER_DIRS__ = [[0,0],[60,0],[60,60],[120,60],[120,120],[180,120],[180,180],[180,240],[240,240],[300,240],[300,300],[300,0]]
    
    
    def __init__(this,startID,direction,trailNum,fn="",graph=None)
        this.super(AlgTrigWalk,this).__init__(fn,graph);
        a = numpy.array(AVAILABLE_DIRECTIONS) #numpy array
        try:
            this.direction = a.tolist().index(direction) 
        except ValueError:
            raise ValueError("This direction is not availale for walking athe moment");
        this.currentID = startID;
        p = graph.getPixel(startID)
        # is the triangle pointing upward?
        if (p.getDirectionDistance(60)==1) || (p.getDirectionDistance(180)==1) || (p.getDirectionDistance(300)==1):
            this.startDir=0
        elif (p.getDirectionDistance(0)==1) || (p.getDirectionDistance(120)==1) || (p.getDirectionDistance(240)==1):
            this.startDir=1
        # else issue a warining?
        this.trail = [startID]
        this.lastIDs = []
        this.trailNum = trailNum

    def step():
        if ~this.isFinished():
            thisDir = this.__INNER_DIRS__[this.direction][this.startDir]
            thisP = graph.getPixel(this.currentID);
            this.currentID = thisP.getDirectionNeighborID(thisDir)
            # update trail
            this.trail.insert(0,currentID)
            this.trail = this.trail[0:trailNum]
            for i in range(len(this.trail))
                this.graph.getPixel(this.trail[i]).setColor([1.0-i/len(this.trail) for k in [0,1,2]]);
    def getactualPosition(this):
        "return the current node."
        return this.currentID
    def isFinished():
        "Check whether there exists a neighbor in walking direction"
        return graph.getPixel(this.currentID).getDirectionDistance(this.__INNER_DIRS__[this.direction][this.startDir]) > 0
        