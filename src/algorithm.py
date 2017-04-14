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
    """
    
    osf = 1
    
    def __init(this,fn="",graph=None):
        "Initialize the algorithm to act on a certain graph object"
        super(Algorithm,this).__init__(fn,graph);
    
    @abstractmethod
    def step(this):
        "perform a step/frame of the algorithm"
        pass

    def getFramerate(this):
        "perform a step only each kth step of the parent algorithm or framerate if this is a main algorithm"
        return this.osf;

    def setFramerate(this,osf):
        "perform a step only each kth step of the parent algorithm"
        this.osf=osf;
        
    @abstractmethod
    def isFinished(this):
        "returns whether this algorithm has finished running"
        pass

    @abstractmethod
    def step(this):
        "perform a step of the algorithm"
        pass

    @abstractmethod
    def getGraphs(this):
        "Returns the array of the graphs the algorithm works on."
        pass

    @abstractmethod
    def getFollowUp(this):
        "if the algorithm is finished it may provide a followUpAlgorithm or set of Algorithms"
        pass

class metaAlgorithm(Algorithm):
    """
    A meta algorithm consists of a set of algorithms that are iterated in each
    step and deleted is finsihed
    """
    def __init__(this,algorithms,fn="",graph=None):
        super(metaAlgorithm,this).__init__(fn,graph)
        this.algorithms = algorithms;
        this.iter = 0;
    
    def step(this):
        if len(this.algorithms) > 0:
            this.iter = this.iter + 1;
            # TODO: check if finished ones have a followUp?
            #remove finished
            this.algorithms = [x for x in this.algorithms if not x.isFinished() ]
            if len(this.algorithms) > 0:
                # step remaining ones
                for x in this.algorithms:
                    if (this.iter%x.getFramerate()) == 0:
                        x.step()
    
    def isFinished(this):
        return len(this.algorithms)==0

class mainAlgorithm(metaAlgorithm):
    """
    The main Algorithms class connects the graph with the view, a Stackenlichten
    and updates the piel after each step, which consists of running all its child algorithms
    """
    def __init__(this,SLC,algorithms,fn="",graph=None):
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
        super(AlgTrigWalkCycle,this).__init__(fn,graph);
        this.startID=startID
        this.directions=directions
        this.actDir = 0
        this.currID = startID
        this.currAlg = AlgTrigWalk(startID,directions[this.actDir],trailNum,fn,graph)
        this.trailNum = trailNum
    
    def step(this):
        this.currAlg.step()
        if this.currAlg.isFinished(): #start next one
            this.actDir = (this.actDir+1)%(len(this.directions))
            curPos = this.currAlg.getactualPosition();
            this.currAlg = AlgTrigWalk(curPos,this.directions[this.actDir],this.currAlg.trail,"",this.currAlg)
        
    def isFinished(this): #infinite loop
        return False

class AlgTrigWalk(Algorithm):
    """
    An algorithm running along a direction starting from a pixel with a tail in
    a colormap
    """
    # we have to alternate, these are for /\ triangles, for \/ start with the
    # second term each entry
    DIRECTION_MAPS = {0:[0,0], 30:[60,0], 60:[60,60], 90:[60,120], 120:[120,120], 150:[180,120], 180:[180,180], 210:[180,240], 240:[240,240], 270:[300,240], 300:[300,300], 330:[300,0]}
    
    
    def __init__(this,startID,direction,trail,fn="",graph=None):
        super(AlgTrigWalk,this).__init__(fn,graph);
        if direction not in AlgTrigWalk.DIRECTION_MAPS:
            raise ValueError("This direction is not availale for walking athe moment");
        this.Direction = direction
        this.currentID = startID;
        p = this.getPixel(startID)
        # is the triangle pointing upward?
        if (p.getDirectionDistance(60)==1) or (p.getDirectionDistance(180)==1) or (p.getDirectionDistance(300)==1):
            this.startDir=0
        elif (p.getDirectionDistance(0)==1) or (p.getDirectionDistance(120)==1) or (p.getDirectionDistance(240)==1):
            this.startDir=1
        # else issue a warining?
        this.trail = trail
        this.trailNum = len(trail)

    def step(this):
        if ~this.isFinished():
            thisDir = this.DIRECTION_MAPS[this.Direction][this.startDir]
            thisP = this.getPixel(this.currentID);
            this.currentID = thisP.getDirectionNeighborID(thisDir)
            # off old trail
            for i in range(len(this.trail)):
                this.getPixel(this.trail[i]).setColor([0.0,0.0,0.0]);
            # update trail
            this.trail.insert(0,this.currentID)
            this.trail = this.trail[0:this.trailNum]
            n = len(this.trail)
            for i in range(n):
                this.getPixel(this.trail[i]).setColor([1.0, 0.3,0.9]);
            # switch step
            this.startDir = (this.startDir+1)%2

    def getactualPosition(this):
        "return the current node."
        return this.currentID

    def isFinished(this):
        "Check whether there exists a neighbor in walking direction"
        return this.getPixel(this.currentID).getDirectionNeighborID(this.DIRECTION_MAPS[this.Direction][this.startDir]) is None
