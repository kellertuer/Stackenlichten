from .Graph import Graph
from .Pixel import Pixel
import numpy as np
import random
import math

def abstractmethod(method):
    def default_abstract_method(*args, **kwargs):
        raise NotImplementedError('call to abstract method ' + repr(method))

    default_abstract_method.__name__ = method.__name__

    return default_abstract_method

class Algorithm(Graph):
    """
    All algorithm serves as decorator for a graph, such that any algorthm may
    keep a list of sub algorithms to be performed within the algorithm.

    The algorithm is also an observer and an observable pattern.
    """

    PARAMS = {"OSF" : 1}
    DIRECTION_MAPS = {0:[0,0], 30:[60,0], 60:[60,60], 90:[60,120], 120:[120,120], 150:[180,120], 180:[180,180], 210:[180,240], 240:[240,240], 270:[300,240], 300:[300,300], 330:[300,0]}

    def __init__(this,graph=None,parameters=None):
        "Initialize the algorithm to act on a certain graph object"
        super(Algorithm,this).__init__(graph)
        this.observers = []
        if parameters is None:
            this.parameters = {} # instanciate a new one!
            for key,value in this.PARAMS.items():
                this.parameters[key] = value
        else:
            this.parameters = parameters
            for key,value in this.PARAMS.items():
                if not key in parameters:
                    this.parameters[key] = value
    @abstractmethod
    def step(this):
        "perform a step/frame of the algorithm"
        pass
    def getFramerate(this):
        "perform a step only each kth step of the parent algorithm or framerate if this is a main algorithm"
        return this.parameters.get("OSF",1);
    def setFramerate(this,osf):
        "perform a step only each kth step of the parent algorithm"
        this.parameters["OSF"]=osf;
    def setParameters(this,parameters):
        for key,value in parameters.items():
            this.parameters[key] = value
    def setParametersOf(this,Indices,parameters):
        this.setParameters(parameters) # end / fallback
    def setParameter(this,key,value):
        this.parameters[key] = value
    def setParameterOf(this,Indices,key,value):
        this.setParameter(key,value) # end / fallback
    def getParameter(this,key):
        return this.parameters.get(key)
    def getParameterOf(this,Indices,key):
        return this.getParameter(key) # end / fallback
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
    def reset(this):
        this.setBlack()
    @abstractmethod
    def update(this, *args, **kwargs):
        pass
    def register(this, observer):
        if not observer in this.observers:
            this.observers.append(observer)
    def unregister(this, observer):
        if observer in this.observers:
            this.observers.remove(observer)
    def unregister_all(this):
        if this.observers:
            del this.observers[:]
    def update_observers(this, *args, **kwargs):
        for observer in this.observers:
            observer.update(*args, **kwargs)

class mainAlgorithm(Algorithm):
    """Main Algorithm
    The main Algorithms class connects the graph with the view, a Stackenlichten
    and updates the piel after each step, which consists of running all its child algorithms
    """
    def __init__(this,SLC,algorithm):
        super(mainAlgorithm,this).__init__(algorithm)
        this.alg = algorithm;
        this.SLC = SLC
    def step(this):
        this.alg.step()
        # put pixels to leds
        this.SLC.render(this.alg)
    def setBlack(this):
        this.alg.setBlack();
        this.SLC.render(this)
    def isFinished(this):
        return this.alg.isFinished()
    def getParameter(this,key):
        this.alg.getParameter(key)
    def update(this, *args, **kwargs):
        this.alg.update(*args, **kwargs)

class metaAlgorithm(Algorithm):
    """ Meta Algorithm
        the meta algorithm just encapsulates a set of algorithms and assumes
        they all work on the same graph, i.e. the last set pixel wins
    """
    def __init__(this,algorithms,graph=None,parameters=None):
        super(metaAlgorithm,this).__init__(graph,parameters)
        this.algorithms = algorithms
        this.iter = 0;
        if parameters is None:
            this.parameters = {"FinishType":"All"}
        else:
            this.parameters = parameters
        if not "FinishType" in this.parameters:
            this.parameters["FinishType"] = "All"
    def step(this):
        if len(this.algorithms) > 0:
            this.iter = this.iter + 1;
            this.algorithms = [x for x in this.algorithms if not x.isFinished() ]
            if len(this.algorithms) > 0:
                # step remaining ones
                for x in this.algorithms:
                    if (this.iter%x.getFramerate()) == 0:
                        x.step()
    def append(algorithm):
        this.algorithms.append(algorithm)
    def reset(this):
        for x in this.algorithms:
            x.reset()
    def isFinished(this):
        if this.parameters["FinishType"] == "All":
            T = [x for x in this.algorithms if not x.isFinished() ]
            v = len(T)==0
        elif this.parameters["FinishType"] == "Any":
            T = [x for x in this.algorithms if not x.isFinished() ]
            v = len(T) < len(this.algorithms)
        return v
    def setParameters(this,parameters):
        for a in this.algorithms:
            a.setParameters(parameters)
    def setParameter(this,key,value):
        for a in this.algorithms:
            a.setParameter(key,value)
    def setParametersOf(this,Indices,parameters):
            if isinstance(Indices,list):
                ind = Indices.pop(0)
                if len(Indices)>0:
                    this.algorithms[ind].setParametersOf(Indices,parameters)
                else:
                    this.algorithms[ind].setParameters(parameters)
            else:
                    this.algorithms[Indices].setParameters(parameters)
    def setParameterOf(this,Indices,key,value):
            if isinstance(Indices,list):
                ind = Indices.pop(0)
                if len(Indices)>0:
                    this.algorithms[ind].setParameterOf(Indices,key,value)
                else:
                    this.algorithms[ind].setParameter(key,value)
            else:
                    this.algorithms[Indices].setParameter(key,value)
    def getParameter(this,key):
        return [this.parameters.get(key), [a.getParameter(key) for a in this.algorithms]]
    def getParameterOf(this,Indices,key):
        if isinstance(Indices,list):
            ind = Indices.pop(0)
            if len(Indices)>0:
                return this.algorithms[ind].getParameterOf(Indices,key,value)
            else:
                return this.algorithms[ind].getParameter(key)
        else:
            return this.algorithms[ind].getParameter(key)
    def update(this, *args, **kwargs):
        for x in this.algorithms:
            x.update(*args, **kwargs)

class iterAlgorithm(Algorithm):
    """ Iter Algorithm
        the meta algorithm just encapsulates a set of algorithms and assumes
        they all work on the same graph, i.e. the last set pixel wins
    """
    def __init__(this,algorithms,graph=None,parameters=None):
        super(iterAlgorithm,this).__init__(graph,parameters)
        this.algorithms = algorithms;
        this.numAlg = 0
        this.actAlg = this.algorithms[0]
        this.iter = 0
    def step(this):
        if len(this.algorithms) > 0:
            this.iter = this.iter + 1;
            if this.actAlg.isFinished():
                this.numAlg += 1
                if this.numAlg < len(this.algorithms):
                    this.actAlg = this.algorithms[this.numAlg]
            if (this.iter%this.actAlg.getFramerate()) == 0:
                this.actAlg.step()
    def append(algorithm):
        this.algorithms.append(algorithm)
    def isFinished(this):
        return this.numAlg == (len(this.algorithms)-1) and len(this.algorithms)==0
    def setParameters(parameters):
        for a in this.algorithms:
            a.setParameters(parameters)
    def setParameter(key,value):
        for a in this.algorithms:
            a.setParameter(key,value)
    def getParameter(key):
        return [a.getParaneter(key) for a in this.algorithms]
    def update(this, *args, **kwargs):
        for a in this.algorithms:
            a.update(*args, **kwargs)

class replicatePixelAlgorithm(Algorithm):
    """
    replicateAlgorithm -- take one algorithm but replicate the result
    from one pixel to several others
    """

    def __init__(this,alg,origID,copyIDs,graph=None,parameters=None):
        super(replicatePixelAlgorithm,this).__init__(graph,parameters)
        this.alg = alg
        this.origID = origID
        this.copyIDs = copyIDs
    def step(this):
        "perform a step/frame of the algorithm"
        this.alg.step()
        c = this.alg.getPixel(this.origID).getColor()
        this.getPixel(this.origID).setColor(c)
        for id in this.copyIDs:
            this.getPixel(id).setColor(c)
    def setParameters(this,parameters):
        this.alg.setParameters(parameters)
    def setParameter(this,key,value):
        this.als.setParameter(key,value)
    def getParameter(this,key):
        return this.alg.getParameter(key)
    def isFinished(this):
        return this.alg.isFinished()

class addAlgorithm(metaAlgorithm):
    def __init__(this,algorithms,graph=None,parameters=None):
        super(addAlgorithm,this).__init__(algorithms,graph,parameters)

    def step(this):
        super(addAlgorithm,this).step()
        if len(this.algorithms) > 0:
            # step remaining ones
            for k in this.nodes.keys():
                this.nodes[k].setColor([0.0,0.0,0.0]);
            for x in this.algorithms:
                for k in this.nodes.keys():
                    this.nodes[k] += x.nodes[k]

class multAlgorithm(metaAlgorithm):
    def __init__(this,algorithms,graph=None):
        super(multAlgorithm,this).__init__(algorithms,graph)

    def step(this):
        super(multAlgorithm,this).step()
        if len(this.algorithms) > 0:
            # start with 1 and multiply them
            for k in this.nodes.keys():
                this.nodes[k].setColor([1.0,1.0,1.0]);
            for x in this.algorithms:
                for k in this.nodes.keys():
                    this.nodes[k] *= x.nodes[k]

class overlayAlgorithm(metaAlgorithm):
    def __init__(this,algorithms,transparentcolors,graph=None):
        super(overlayAlgorithm,this).__init__(algorithms,graph)
        this.tColors = transparentcolors

    def step(this):
        super(overlayAlgorithm,this).step()
        if len(this.algorithms) > 0:
            # start with 1 and multiply them
            for k in this.nodes.keys():
                this.nodes[k].setColor(this.tColors[0]);
            c=0
            for x in this.algorithms:
                trColor = this.tColors[c]
                for k in this.nodes.keys():
                    thisC = x.nodes[k].getColor()
                    if thisC!=trColor:
                        this.nodes[k].setColor(thisC)
                c = c+1

class sequentialAlgorithm(metaAlgorithm):
    """An Algorithm to perform sequential execution of an array of algorithms
    """
    def __init__(this,algorithms,repeat=False,graph=None,parameters=None):
        super(sequentialAlgorithm,this).__init__(algorithms,graph,parameters)
        this.repeat = repeat
        this.actAlgorithm = 0

    def step(this):
        if this.algorithms[this.actAlgorithm].isFinished():
            if this.actAlgorithm < len(this.algorithms)-1:
                this.actAlgorithm = this.actAlgorithm + 1
                this.algorithms[this.actAlgorithm].reset()
                # and for the last fnished?
            elif this.repeat:
                this.actAlgorithm=0
                this.algorithms[this.actAlgorithm].reset()
        #step.
        this.algorithms[this.actAlgorithm].step()
        this.setBlack()
        for k in this.algorithms[this.actAlgorithm].nodes.keys():
            this.nodes[k] += this.algorithms[this.actAlgorithm].nodes[k]

    def isFinished(this):
        # no repeats, last algorithm was active and has finished
        return (not this.repeat) and (this.actAlgorithm == len(this.algorithms)-1) and (this.algorithms[-1].isFinished())
#
#
#
# Specific algorithms
#-------------------------------------------------------------------------------
class AlgPause(Algorithm):
    """A simple short pause algorithm to pause between sequential algorithms
       can also be used to have an indefinite pause by using AlgPause(0)
    """
    def __init__(this,duration,graph=None):
        super(AlgPause,this).__init__(graph)
        this.parameters["PauseDuration"] = duration
        this.cnt = 0
    def step(this):
        # cnt=0,pause=0 means infinite pause...
        if this.parameters["PauseDuration"]>0:
            this.cnt = this.cnt + 1
    def isFinished(this):
         return this.cnt > this.parameters["PauseDuration"]
    def setParameters(this,parameters):
        super(AlgPause,this).setParameters(parameters)
        this.__updateState()
    def setParameter(this,key,value):
        super(AlgPause).setParameter(key,value)
        this.__updateState()
    def __updateState(this):
        if this.parameters.get("EndPause",False):
            this.cnt = this.parameters["PauseDuration"]+1
        if this.parameters.get("StartPause",False):
            this.cnt = 0
    def update(this, *args, **kwargs):
        d=args[0];
        if isinstance(d,dict):
            this.setParameters(d)

class AlgBackground(Algorithm):
    """ Background Algorithm
    The background algorithm just sets a constant color as background.
    In the meta Algorithm it should hence be set as first algorithm.
    """
    def __init__(this,color=[0,0,0],graph=None):
        super(AlgBackground,this).__init__(graph)
        this.color= color
    def step(this):
        for k,n in this.nodes.items():
            n.setColor(this.color)
    def isFinished(this):
        return False
    def update(this, *args, **kwargs):
        pass

class AlgDisplayDigit(Algorithm):
    """An hardcoded algorithm to display italic numbers
    (keep dirRight to 90, dirDown to 210 if you'Re unsure)
    the posTopLeft should be an uowards pointing triangle.
    Digits do not run over the (special) boundary.
    """
    # HARDCODED!
    DIGITS = [
        #0
        [[1,1,1,1,1,0],[1,1,0,0,1,1],[1,1,0,0,1,1],[1,1,0,0,1,1],[0,1,1,1,1,1]],
        #1
        [[0,1,1,1,0,0],[0,0,1,1,0,0],[0,0,1,1,0,0],[0,0,1,1,0,0],[0,1,1,1,1,0]],
        #2
        [[1,1,1,1,1,0],[0,0,0,0,1,1],[1,1,1,1,1,1],[1,1,0,0,0,0],[1,1,1,1,1,0]],
        #3
        [[0,1,1,1,1,0],[0,0,0,0,1,1],[0,0,0,1,1,1],[0,0,0,0,1,1],[0,1,1,1,1,1]],
        #4
        [[1,1,0,0,1,1],[1,1,0,0,1,1],[0,1,1,1,1,1],[0,0,0,0,1,1],[0,0,0,0,1,1]],
        #5
        [[1,1,1,1,1,0],[1,1,0,0,0,0],[1,1,1,1,1,0],[0,0,0,0,1,1],[0,1,1,1,1,1,]],
        #6
        [[1,1,1,1,0,0],[1,1,0,0,0,0],[1,1,1,1,1,0],[1,1,0,0,1,1],[0,1,1,1,1,1]],
        #7
        [[0,1,1,1,1,1],[0,0,0,0,1,1],[0,0,0,0,1,1],[0,0,0,0,1,1],[0,0,0,0,1,1]],
        #8
        [[1,1,1,1,1,0],[1,1,0,0,1,1],[1,1,1,1,1,1],[1,1,0,0,1,1],[0,1,1,1,1,1]],
        #9
        [[1,1,1,1,1,0],[1,1,0,0,1,1],[0,1,1,1,1,1],[0,0,0,0,1,1],[0,0,1,1,1,1]],
        #10-white
        [[1,1,1,1,1,1],[1,1,1,1,1,1],[1,1,1,1,1,1],[1,1,1,1,1,1],[1,1,1,1,1,1]]]
    def __init__(this,digit,posTopLeft,duration,dirRight=90,dirDown=210,graph=None):
        super(AlgDisplayDigit,this).__init__(graph)
        this.parameters["DisplayDigitDuration"] = duration
        this.parameters["Digit"] = digit
        this.parameters["Name"] = "NormalDigit"
        this.TLID = posTopLeft
        this.dirRight = dirRight
        this.dirDown = dirDown
        this.reset()
    def reset(this):
        super(AlgDisplayDigit,this).reset()
        this.parameters["EndDisplayDigit"] = False
        this.cnt = 0
    def step(this):
        # cnt=0,pause=0 means infinite pause...
        # put digit on the graph if valid number
        if this.getParameter("Digit")>=0 and this.getParameter("Digit")<=10:
            thisDigit = this.DIGITS[this.getParameter("Digit")]
            firstInLineID = this.TLID
            for i,row in enumerate(thisDigit):
                thisID = firstInLineID
                for j,entry in enumerate(row):
                    p = this.getPixel(thisID)
                    p.setColor([float(entry)]*3)
                    # is the triangle pointing upward?
                    if (p.getDirectionDistance(60)==1) or (p.getDirectionDistance(180)==1) or (p.getDirectionDistance(300)==1):
                        this.startDir=0 #
                    elif (p.getDirectionDistance(0)==1) or (p.getDirectionDistance(120)==1) or (p.getDirectionDistance(240)==1):
                        this.startDir=1
                    nextDir = thisDir = this.DIRECTION_MAPS[this.dirRight][this.startDir]
                    thisID = p.getDirectionNeighborID(nextDir)
                    if thisID is None:
                        break# end this line
                # switch to next line
                p = this.getPixel(firstInLineID)
                firstInLineID = p.getDirectionNeighborID(this.dirDown)
                if firstInLineID is None:
                    break #if no next line available -> break setting
            if this.parameters.get("DisplayDigitDuration",0)>0:
                this.cnt = this.cnt + 1
    def isFinished(this): # finishes exactely once
        return this.cnt > this.parameters.get("DisplayDigitDuration",0)
    def setParameters(this,parameters):
        super(AlgDisplayDigit,this).setParameters(parameters)
        this.__updateState()
    def setParameter(this,key,value):
        super(AlgDisplayDigit,this).setParameter(key,value)
        this.__updateState()
    def __updateState(this):
        if this.parameters.get("EndDisplayDigit",False):
            this.cnt = this.parameters["DisplayDigitDuration"]+1
        if this.parameters.get("StartPause",False):
            this.cnt = 0
    def update(this, *args, **kwargs):
        d=args[0];
        if isinstance(d,dict):
            if (not 'Digit' in d) or (d.get('Name','') == this.getParameter('Name')):
                this.setParameters(d)

class AlgDiffusion(Algorithm):
    """Algorithm to perform Diffusion on the colors
    """
    def __init__(this,stepSize=0.05,graph=None):
        super(AlgDiffusion,this).__init__(graph)
        this.stepSize = stepSize
        this.algInit = False
    def step(this):
        gCopy = this.clone()
        for k in this.nodes.keys():
            csub = [0,0,0]
            numN = 0.5 #len(this.nodes[k].getNeighborIDs())
            for l in this.nodes[k].getNeighborIDs():
                c = gCopy.nodes[k].getColor()
                c2 = gCopy.nodes[l].getColor()
                step = [i - j for i, j in zip(c, c2)]
                csub = [csub[i] - step[i]*this.stepSize/numN for i in range(3)]
                this.nodes[l].addToColor([step[i]*this.stepSize for i in range(3)])
            this.nodes[k].addToColor(csub)
        this.algInit = True
    def isFinished(this):
        if not this.algInit:
            return False
        init = False
        finished = True
        for k in this.nodes.keys():
            if not init:
                c = this.nodes[k].getColor()
                init = True
            else:
                c2 = this.nodes[k].getColor()
                for i in range(3):
                    if not c2[i] == c[i]:
                        finished=False
        return finished
    def update(this, *args, **kwargs):
        pass

class AlgRandomPoint(Algorithm):
    """A class modelling a (random) point with (random) fade in, duration, and fadeout.
    """
    def __init__(this,graph=None,parameters=None):
        super(AlgRandomPoint,this).__init__(graph,parameters)
        this.repeat = this.parameters.get("repeat",False)
        this.newRand = this.parameters.get("repeatrandom",False)
        this.randStyle = this.parameters.get("randomPositionStyle","global")
        this.ID = this.parameters.get("ID",0)
        #choice of global vs neighbor
        this.reset(True)

    def reset(this,newRand=False):
        if newRand:

            if this.parameters.get("ID",0) > 0:
                this.ID = this.parameters["ID"]
            else:
                if this.ID > 0 and this.randStyle=="neighbor": # we have a position and look for a random neighbor
                    this.ID = random.choice(this.getPixel(this.ID).getNeighborIDs())
                else: #this.randStyle == "global" or no first ID yet;
                    this.ID = random.choice(range(1,this.getNumNodes()))
            if this.parameters.get("fadein_variance",0) > 0:
                this.fadein = max(round(random.gauss(this.parameters.get("fadein",0),this.parameters.get("fadein_variance",0))),0)
            else:
                this.fadein = this.parameters.get("fadein",0)
            if this.parameters.get("fadeout_variance",0) > 0:
                this.fadeout = max(round(random.gauss(this.parameters.get("fadeout",0),this.parameters.get("fadeout_variance",0))),0)
            else:
                this.fadeout = this.parameters.get("fadeout",0)
            if this.parameters.get("duration_variance",0) > 0:
                this.duration = max(round(random.gauss(this.parameters.get("duration",0),this.parameters.get("duration_variance",0))),0)
            else:
                this.duration = this.parameters.get("duration",0)
            if this.parameters.get("pause_variance",0) > 0:
                this.pause = max(round(random.gauss(this.parameters.get("pause",0),this.parameters.get("pause_variance",0))),0)
            else:
                this.pause = this.parameters.get("pause",0)
            # scale?
            s = this.parameters.get("scale",1)
            if  s > 1:
                this.fadein = this.fadein*s
                this.duration = this.duration*s
                this.fadeout = this.fadeout*s
                this.pause = this.pause*s
            this.lengths = [this.fadein, this.fadein+this.duration, this.fadein+this.duration+this.fadeout, this.fadein+this.duration+this.fadeout+this.pause]
        this.count=0

    def step(this):
        if (this.count < this.lengths[3]):
            this.count = this.count + 1
            if this.count <= this.lengths[0]: # fade_in
                if this.fadein > 0:
                    v = float(this.count)/float(this.fadein)
                else:
                    v=0.0;
            elif this.count <= this.lengths[1]: # on
                v = 1.0
            elif this.count <= this.lengths[2]: # fadeout
                if this.fadeout>0:
                    v = float(this.lengths[2]-this.count)/float(this.fadeout)
                else:
                    v = 0.0;
            else: #out/pause
                v = 0.0
            this.getPixel(this.ID).setColor([v,v,v])
            if this.count==this.lengths[3]: #last step?
                if this.repeat:
                    this.reset(this.newRand)

    def isFinished(this):
        return not ( (this.count < this.lengths[3]) and this.repeat)

class AlgRandomPoints(Algorithm):
    """AlgRandomPoints – generate (and destruct)
    """
    def __init__(this,destruct=0,maxNum=10,createEvery=1,graph=None):
        super(AlgRandomPoints,this).__init__(graph)
        this.destruct = destruct
        this.maxNum = maxNum;
        this.iter = 0
        this.num = 0
        this.createEvery = createEvery
        if destruct > 0:
            this.alive = dict()
            for k in this.nodes.keys():
                this.alive[k]=0
    def step(this):
        if this.destruct > 0:
            for k in this.alive.keys():
                if this.alive[k]>0:
                    this.alive[k] -= 1
                    if this.alive[k] == 0:
                        this.nodes[k].setColor([0,0,0])
        if (this.iter%this.createEvery) == 0 and (this.maxNum==0 or this.num < this.maxNum):
            this.num += 1
            k = random.choice(list(this.nodes.keys()))
            c = [random.random() for i in range(3)]
            this.nodes[k].setColor(c)
            if this.destruct > 0:
                this.alive[k] = random.randint(1,this.destruct)
        this.iter +=1
    def isFinished(this):
        finished = (this.num==this.maxNum) and this.maxNum>0
        if this.destruct > 0:
            for k in this.alive.keys():
                if this.alive[k] > 0:
                    finished = False
        return finished
    def update(this, *args, **kwargs):
        pass

class AlgFadeOut(Algorithm):
    def __init__(this,frames=30,graph=None):
        super(AlgFadeOut,this).__init__(graph)
        this.actFrame=0
        this.frames = frames
    def step(this):
        this.actFrame +=1
        for k,n in this.nodes.items():
            n.brightness = float(this.frames-this.actFrame)/float(this.frames)
    def isFinished(this):
        return this.actFrame==this.frames
    def update(this, *args, **kwargs):
        pass

class AlgSampleFunction(Algorithm):
    """Algorithm to Sample a Function
        A function f(x,y,p) is sampled on (x,y)-plane with respect to the
        directions and distances of the nodes. This function is enhances by
        parameters and accompanied by a stepParameters function."""
    def __init__(this,fct,stepParamFct,initParameters,graph=None):
        super(AlgSampleFunction,this).__init__(graph)
        this.function = fct
        this.stepFct = stepParamFct
        this.FctValues = initParameters
    def step(this):
        finished = False
        sampledList = dict()
        positions = dict()
        for k in this.nodes.keys():
            sampledList[k] = False
        Start = True
        samplePoint = [0,0];
        while not finished:
            for k,n in this.nodes.items(): #k neighbor id, n its index
                if not sampledList[k]:
                    if Start:
                        nextID = k
                        dir = 0
                        dist = 0
                        Start = False
                        positions[k] = samplePoint
                        break
                    else:
                        found=False
                        for k2 in sampledList.keys():
                            if sampledList[k2]:
                                if this.nodes[k2].isNeighbor(n) and this.nodes[k2].getNeighborDistance(n)>0:
                                    nextID = k
                                    dir = this.nodes[k2].getNeighborDirection(n)
                                    dist = this.nodes[k2].getNeighborDistance(n)
                                    samplePoint = positions[k2]
                                    positions[k] = [samplePoint[0] + np.sin(dir/180.0*np.pi)*dist,samplePoint[1] + np.cos(dir/180.0*np.pi)*dist]
                                    found=True
                                    break
                        if found:
                            break
            # updirection is 0 degree, hence we invert sin and cos
            this.nodes[nextID].setColor(this.function(positions[nextID],this.FctValues))
            sampledList[nextID] = True
            finished = True
            for k in sampledList.keys():
                finished = finished & sampledList[k]
        this.FctValues = this.stepFct(this.FctValues)
    def isFinished(this):
        this.FctValues.get('finished',False)
    def update(this, *args, **kwargs):
        pass

class AlgRunningLight(Algorithm):
    """The algorithm performs a simple running light ordered by id"""
    def __init__(this,randomColor=True,restart=True,sort=False,graph=None):
        """Initialize the Runninglight.
        Variables:
        * randomColor – random color (if set true)
        * repeatSequence - repeat or not"""
        super(AlgRunningLight,this).__init__(graph)
        this.sort = sort
        if sort:
            this._iterator = iter(sorted(this.nodes.keys()))
        else:
            this._iterator = iter(this.nodes.keys())
        this.restart = restart
        this.currentID = None
        this.start = True
    def step(this):
        this.start=False
        if this.currentID is not None:
            #remove last
            this.getPixel(this.currentID).setColor([0, 0,0])
        try:
            this.currentID = this._iterator.__next__()
        except StopIteration:
            this.currentID = None
        if this.currentID is not None:
            this.getPixel(this.currentID).setColor([1.0, 1.0,1.0]);
        elif this.restart:
            if this.sort:
                this._iterator = iter(sorted(this.nodes.keys()))
            else:
                this._iterator = iter(this.nodes.keys())
            this.start = True
    def isFinished(this):
        return this.currentID is None and this.start == False
    def getPosition(this):
        "return the current node."
        return this.currentID
    def update(this, *args, **kwargs):
        pass

class AlgTrigWalkCycle(Algorithm):
    """The algorithm to run in circles on the trig grid. Following a direction
    until the border and continuing with the next direction; cycling through these.
    """
    def __init__(this,startID,directions,trailNum,lookaheads=None,graph=None):
        super(AlgTrigWalkCycle,this).__init__(graph);
        this.startID=startID
        this.directions=directions
        if lookaheads is None:
            this.lookaheads = [0]*len(directions)
        else:
            this.lookaheads = lookaheads
        this.actDir = 0
        this.currID = startID
        this.currAlg = AlgTrigWalk(startID,directions[this.actDir],trailNum,this.lookaheads[this.actDir],graph)
        this.trailNum = trailNum
    def step(this):
        if this.currAlg.isFinished(): #start next one
            this.actDir = (this.actDir+1)%(len(this.directions))
            curPos = this.currAlg.getPosition();
            this.currAlg = AlgTrigWalk(curPos,this.directions[this.actDir],this.currAlg.trail,this.lookaheads[this.actDir],this.currAlg)
        this.currAlg.step()
    def isFinished(this): #infinite loop
        return False
    def update(this, *args, **kwargs):
        pass

class AlgTrigWalk(Algorithm):
    """
    An algorithm running along a direction starting from a pixel with a tail in
    a colormap
    """
    # we have to alternate, these are for /\ triangles, for \/ start with the
    # second term each entry
    def __init__(this,startID,direction,trail,lookahead=1,graph=None):
        super(AlgTrigWalk,this).__init__(graph)
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
        this.lookahead=lookahead
    def step(this):
        if not this.isFinished():
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
                this.getPixel(this.trail[i]).setColor([1.0, 1.0,1.0]);
            # switch step
            if thisP.getDirectionDistance(thisDir) > 0: # not special boundary
                this.startDir = (this.startDir+1)%2 # only change in normal cases
    def getPosition(this):
        "return the current node."
        return this.currentID
    def isFinished(this):
        "Check whether there exists a neighbor in walking direction"
        cnt = 0
        checkID = this.currentID
        while cnt < this.lookahead:
            checkID = this.getPixel(checkID).getDirectionNeighborID(this.DIRECTION_MAPS[this.Direction][(this.startDir+cnt)%2])
            cnt = cnt+1
            if checkID is None:
                return True
        return False
    def update(this, *args, **kwargs):
        pass

class AlgRandomBlink(Algorithm):
    """
    An algorithm producing random blinks within the graph of given or random
    or random duration abd pause
    """
    def __init__(this,meanBlinkIntervall,BlinkRandom,meanBlinkLength,BlinkLengthVariance,graph=None):
        super(AlgRandomBlink,this).__init__(graph)
        this.blinkP=meanBlinkIntervall
        this.blinkR = BlinkRandom
        this.blinkL = meanBlinkLength
        this.blinkLVar = BlinkLengthVariance
        this.activeNodes = []
        this.activeFramesLeft = []
        if this.blinkR:
            this.nextTime = int(math.floor(-this.blinkP*math.log(random.uniform(0, 1))))
        else:
            this.nextTime = meanBlinkIntervall
        this.cnt = 0;
    def isFinished(this):
        return False
    def step(this):
        # draw random number to determine whether a new pixel is lit
        this.cnt = this.cnt+1;
        if (this.cnt==this.nextTime):
            # time to activate next one
            nextNode = random.randint(1,len(this.nodes))
            nextDuration = random.randint(this.blinkL-this.blinkLVar,this.blinkL+this.blinkLVar);
            this.activeNodes.append(nextNode)
            this.activeFramesLeft.append(nextDuration)
            #set Black activate
            if this.blinkR:
                this.nextTime = this.cnt+int(math.floor(-this.blinkP*math.log(random.uniform(0, 1))))
            else:
                this.nextTime = this.cnt+meanBlinkIntervall
            if (this.nextTime==this.cnt):
                this.nextTime = this.nextTime+1
        this.setBlack()
        for i in this.activeNodes:
            this.getPixel(i).setColor([1.0, 1.0,1.0]);
        newN = []
        newD = []
        # which ones not to activcate next time?
        for index, item in enumerate(this.activeFramesLeft):
            if item!=0:
                newN.append(this.activeNodes[index])
                newD.append(item-1)
        this.activeFramesLeft = newD
        this.activeNodes = newN
    def update(this, *args, **kwargs):
        pass

class AlgBasicRobot(Algorithm):
    DIRECTION_MAPS = {
        30:[60,0], 90:[60,120], 150:[180,120],
        210:[180,240], 270:[300,240], 330:[300,0]}

    def __init__(this,startID,trackWalker,graph=None,parameters=None):
        super(AlgBasicRobot,this).__init__(graph,parameters)
        this.startID=startID
        this.parameters["color"] = [0.0,0.7,0.0]
        this.walker = trackWalker
        this.walker.register(this)
        this.reset()
    def reset(this):
        this.positionID = this.startID
        this.parameters["Alive"] = True
        this.highlight=0
    def directionID(this,ID):
        p = this.getPixel(this.positionID)
        # is the triangle pointing upward?
        if (p.getDirectionDistance(60)==1) or (p.getDirectionDistance(180)==1) or (p.getDirectionDistance(300)==1):
            startDir=0
        elif (p.getDirectionDistance(0)==1) or (p.getDirectionDistance(120)==1) or (p.getDirectionDistance(240)==1):
            startDir=1
        return startDir
    def step(this):
        this.setBlack()
        if this.parameters["Alive"]:
            if this.highlight>0:
                this.highlight = this.highlight - 1
                c = this.parameters["color"]
                c[2] = 1.0;
            else:
                c = this.parameters["color"]
            this.getPixel(this.positionID).setColor(c)
    def setParameters(this,parameters):
        super(AlgBasicRobot,this).setParameters(parameters)
        if parameters.get("Position"): # move player involved
            this.setParameter("Position", this.parameters["Position"])
    def setParameter(this,key,value):
        super(AlgBasicRobot,this).setParameter(key,value)
        if key=="Position":
            walkerID = value
            #yay I may move!
            d = random.choice([30,90,150,210,270,330])
            while not this.hasNextNeighbor(d):
                d = random.choice([30,90,150,210,270,330])
            checkID = this.positionID
            startDir = this.directionID(this.positionID)
            this.positionID = this.getPixel(checkID).getDirectionNeighborID(this.DIRECTION_MAPS[d][startDir])
            this.update_observers({"Position":this.positionID})
            if this.walker.getPosition() == this.positionID:
                this.highlight=2
                this.walker.setParameter("Die",True)
        if key=="Die" and value:
            this.parameters["Alive"]=False
    def getPosition(this):
        "return the current node."
        return this.positionID
    def hasNextNeighbor(this,direction):
        "Check whether there exists a neighbor in walking direction"
        checkID = this.positionID
        startDir = this.directionID(this.positionID)
        checkID = this.getPixel(checkID).getDirectionNeighborID(this.DIRECTION_MAPS[direction][startDir])
        return not (this.isFinished() or (checkID is None))
    def isFinished(this):
        return not this.parameters["Alive"]
    def update(this, *args, **kwargs):
        d=args[0];
        if isinstance(d,dict):
            this.setParameters(d)

class AlgWalker(Algorithm):
    """An algorithm to move your player and react to robots"""
    DIRECTION_MAPS = {
        30:[60,0], 90:[60,120], 150:[180,120],
        210:[180,240], 270:[300,240], 330:[300,0]}

    def __init__(this,startID,graph=None,parameters=None):
        super(AlgWalker,this).__init__(graph,parameters)
        this.startID = startID
        this.reset()
    def reset(this):
        this.positionID = this.startID
        this.parameters["Alive"]=True
        this.parameters["Gamescore"]= 0;
        this.highlight=0
    def directionID(this):
        p = this.getPixel(this.positionID)
        # is the triangle pointing upward?
        if (p.getDirectionDistance(60)==1) or (p.getDirectionDistance(180)==1) or (p.getDirectionDistance(300)==1):
            startDir=0
        elif (p.getDirectionDistance(0)==1) or (p.getDirectionDistance(120)==1) or (p.getDirectionDistance(240)==1):
            startDir=1
        return startDir
    def step(this):
        this.setBlack()
        if this.parameters["Alive"]:
            if this.highlight>0:
                this.highlight = this.highlight - 1
                c = [0.0,0.0,1.0]
            else:
                c = [0.8,0.8,0.8]
            this.getPixel(this.positionID).setColor(c)
    def setParameters(this,parameters):
        super(AlgWalker,this).setParameters(parameters)
        if parameters.get("Direction"): # move player involved
            this.setParameter("Direction", this.parameters["Direction"])
        if parameters.get("Die") and this.parameters["Die"]:
            this.setParameter("Die",True)
    def setParameter(this,key,value):
        super(AlgWalker,this).setParameter(key,value)
        if key=="Direction":
            if this.hasNextNeighbor(value):
                checkID = this.positionID
                startDir = this.directionID()
                this.getPixel(checkID).getDirectionNeighborID(this.DIRECTION_MAPS[value][startDir])
            else:
                this.highlight=2
            if this.parameters["Alive"]:
                this.update_observers({"Position":this.positionID})
            this.parameters["Gamescore"] = this.parameters["Gamescore"]+1;
        if key=="Die" and value:
            this.parameters["Alive"] = False
            n = this.parameters["Gamescore"]
            nStr = str(n)
            this.update_observers({'Gamescore':this.parameters["Gamescore"]})
            if n>9:
                this.update_observers({'Name':'Tens','Digit':int(nStr[0])})
                this.update_observers({'Name':'Ones','Digit':int(nStr[1])})
            else: # disable 10th
                this.update_observers({'Name':'Tens','Digit':-1})
                this.update_observers({'Name':'Ones','Digit':int(nStr)})
    def getPosition(this):
        "return the current node."
        return this.positionID
    def hasNextNeighbor(this,direction):
        "Check whether there exists a neighbor in walking direction"
        checkID = this.positionID
        startDir = this.directionID(this.positionID)
        checkID = this.getPixel(checkID).getDirectionNeighborID(this.DIRECTION_MAPS[direction][startDir])
        return not (this.isFinished() or (checkID is None))
    def isFinished(this):
        return not this.parameters["Alive"]
    def update(this, *args, **kwargs):
        d=args[0];
        if isinstance(d,dict):
            this.setParameters(d)

class AlgSnake(Algorithm): #(AlgTrigWalkAlgorithm):
    """
    An algorithm running along a direction starting from a pixel with a tail#
    """
    # we have to alternate, these are for /\ triangles, for \/ start with the
    # second term each entry
    DIRECTION_MAPS = {
        30:[60,0], 90:[60,120], 150:[180,120],
        210:[180,240], 270:[300,240], 330:[300,0]}
    def __init__(this,startID,StartDirection,InitLength,graph=None,parameters=None):
        super(AlgSnake,this).__init__(graph,parameters)
        if StartDirection not in AlgSnake.DIRECTION_MAPS:
            raise ValueError("This direction is not available for walking.");
        parameters = {"StartDirection":StartDirection,"StartID":startID,"StepInt":15,"StartLength":InitLength}
        for k,v in parameters.items():
            if k not in this.parameters:
                this.parameters[k] = v
                #StepInt = 1/Speed
        this.reset()
    def reset(this):
        super(AlgSnake,this).reset()
        this.parameters["Direction"] = this.parameters["StartDirection"]
        this.parameters["CurrentHead"] = this.parameters["StartID"]
        this.parameters["Gamescore"] = 0
        this.parameters["Alive"] = True
        this.parameters["StepInt"] = 15
        this.parameters["pearColor"] = [1.0,0.0,0.0]
        this.parameters["snakeColor"] = [1.0,1.0,1.0]
        this.headID = this.parameters["StartID"]
        p = this.getPixel(this.headID)
        # is the triangle pointing upward?
        if (p.getDirectionDistance(60)==1) or (p.getDirectionDistance(180)==1) or (p.getDirectionDistance(300)==1):
                    this.startDir=0
        elif (p.getDirectionDistance(0)==1) or (p.getDirectionDistance(120)==1) or (p.getDirectionDistance(240)==1):
                this.startDir=1
        this.trail = [this.parameters["StartID"]]*this.parameters["StartLength"]
        this.trailNum = this.parameters["StartLength"]
        this.cnt = 0
        this.warning=False
        this.fruitID = this.headID
        while this.fruitID in this.trail:
            this.fruitID = random.choice([this.nodes[k].ID for k in this.nodes.keys()])
    def step(this):
        notify = False
        if this.cnt==0:
            if this.hasNextNeighbor():
                thisDir = this.DIRECTION_MAPS[this.parameters["Direction"]][this.startDir]
                thisP = this.getPixel(this.headID);
                #this collision tests
                newHead = thisP.getDirectionNeighborID(thisDir)
                if (newHead in this.trail) and (newHead != this.trail[1]):
                    # and not second, in order to not get stuck in corners
                    if this.warning:
                        this.parameters["Alive"] = False
                        notify=True
                    else:
                        this.warning = True
                this.headID = thisP.getDirectionNeighborID(thisDir)
                if thisP.getDirectionDistance(thisDir) > 0: #only switch if not on special boundary
                    this.startDir = (this.startDir+1)%2
                if thisP.getDirectionDistance(thisDir) == -2: #mirror boundary, switch also direction
                    this.parameters["Direction"] = (this.parameters["Direction"]+180)%360
                # off old trail
                for i in range(len(this.trail)):
                    this.getPixel(this.trail[i]).setColor([0.0,0.0,0.0]);
                # update trail
                this.trail.insert(0,this.headID)
                this.trail = this.trail[0:this.trailNum]
                n = len(this.trail)
                for i in range(n):
                    this.getPixel(this.trail[i]).setColor(this.parameters["snakeColor"]);
                if this.fruitID==this.headID:
                    this.setParameter("Gamescore", this.getParameter("Gamescore")+1)
                    while this.fruitID in this.trail:
                        this.fruitID = random.choice([this.nodes[k].ID for k in this.nodes.keys()])
                    this.trailNum = this.trailNum+1 # longer
                    if this.parameters["StepInt"] > 1:
                        this.parameters["StepInt"] = this.parameters["StepInt"]-1 #faster
                this.getPixel(this.fruitID).setColor(this.parameters["pearColor"])
            else: # wallcollision?
                if this.warning:
                    this.parameters["Alive"] = False
                    notify=True
                else:
                    this.warning = True
        # switch step
        this.cnt = (this.cnt+1)%(this.parameters["StepInt"])
        if notify:
            n = this.parameters["Gamescore"]
            nStr = str(n)
            this.update_observers({'Gamescore':this.parameters["Gamescore"]})
            if n>9:
                this.update_observers({'Name':'Tens','Digit':int(nStr[0])})
                this.update_observers({'Name':'Ones','Digit':int(nStr[1])})
            else: # disable 10th
                this.update_observers({'Name':'Tens','Digit':-1})
                this.update_observers({'Name':'Ones','Digit':int(nStr)})
    def setParameters(this,parameters):
        super(AlgSnake,this).setParameters(parameters)
        if parameters.get("Direction") or parameters.get("Rotate"):
            this.warning=False
        this.parameters["Direction"] = (this.parameters["Direction"] + this.parameters.get("Rotate",0))%360
    def setParameter(this,key,value):
        super(AlgSnake,this).setParameter(key,value)
        if key=="Direction" or key=="Rotate":
            this.warning=False
        if key=="Rotate":
            this.parameters["Direction"]=(this.parameters["Direction"]+value)%360
    def getPosition(this):
        "return the current node."
        return this.headID
    def hasNextNeighbor(this):
        "Check whether there exists a neighbor in walking direction"
        checkID = this.headID
        checkID = this.getPixel(checkID).getDirectionNeighborID(this.DIRECTION_MAPS[this.parameters["Direction"]][this.startDir])
        return not (this.isFinished() or (checkID is None))
    def isFinished(this):
        return not this.parameters["Alive"]
    def update(this, *args, **kwargs):
        d=args[0];
        if isinstance(d,dict):
            this.setParameters(d)
