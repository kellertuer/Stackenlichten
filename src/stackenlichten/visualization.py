import sys
import numpy as np
from .Graph import Graph
from .opc import Client
import matplotlib.pyplot as plt
import matplotlib.collections as mpc
import pygame
import time
import turtle as t

def abstractmethod(method):
    def default_abstract_method(*args, **kwargs):
        raise NotImplementedError('call to abstract method ' + repr(method))

    default_abstract_method.__name__ = method.__name__

    return default_abstract_method

class SLV:
    "StackenLichtenVisualization - the connector to the USB board"

    PARAMETERS = {"framerate":50, "Brightness":255}

    def __init__(this,parameters=None):
        this.parameters = SLV.PARAMETERS.copy()
        if parameters is not None:
            this.parameters.update(parameters)

    @abstractmethod
    def render(this, graph,scale=1):
        "render(graph) – renders a graph onto the Stackenlichten and activates the LEDs."
        pass

class FadecandySLV(SLV):
    client = None

    def __init__(this,url='localhost:7890',parameters=None):
        """
        FadecandySLC() initializes the Open Pixel Control (OPC) to connect to
        the usual localhost fadecandy server.
        """
        super(FadecandySLV,this).__init__(parameters)
        print("""                              ~~~ Stackenlichten ~~~
           Let\'s blink in lichten. But with German stacken and blochen.
                                                                     @kellertuer
        Moin.""")
        this.client = Client(url)

    def render(this, graph,scale=1):
        data = [ (0,0,0) ] * 512
        for k in graph.nodes.keys():
            v = [i*scale*this.MAX_BRIGHTNESS*graph.nodes[k].brightness for i in graph.nodes[k].getColor()]
            if k > 512:
                 raise ValueError("The graph node id " + str(k) * " is too large for the fadecandy board (max 512 LEDs).\nPlease reorder or reduce the number")
            data[k-1] = tuple( np.round(v) )
        this.client.put_pixels(data)
        time.sleep(1/this.parameters["framerate"])

class PyTurtleSLV(SLV):

    def __init__(this,length=30,parameters=None):
        """
        PyTurtleSLV() initialize the vizualization using the python turtle module
        """
        super(PyTurtleSLV,this).__init__(parameters)
        print("""                              ~~~ Stackenlichten ~~~
           Let\'s blink in lichten. But with German stacken and blochen AND Turtles!
                                                                    @kellertuer
        Moin.""")
        this.length=length;
        t.home()
        t.mode("logo")
        t.speed(0)
        t.ht()

    def triangleAt(this,pos=(0.0,0.0),dir=90,length=15,fill=(1.0,1.0,1.0),clockwise=True):
        t.color( (0,0,0), fill)
        height = np.sqrt(3)/6*length
        t.pu()
        t.setpos(pos)
        t.setheading(dir)
        t.right(90)
        if clockwise:
            t.backward(height)
        else:
            t.forward(height)
        t.right(90)
        t.forward(length/2)
        t.right(180)
        t.pd();
        t.begin_fill()
        for x in range(3):
            t.forward(length)
            if clockwise:
                t.right(120)
            else:
                t.left(120)
        t.end_fill()
        t.pu()
        t.forward(length/2)
        t.left(90)
        t.forward(height)
        t.left(90)
        t.pd()

    def render(this,graph):
        t.tracer(0, 0)
        t.reset()
        t.ht()
        finished = False
        drawnList = dict()
        upward = dict()
        for k in graph.nodes.keys():
            drawnList[k] = False
        Start = True
        samplePoint = [0.0,0.0]
        while not finished:
            # look for next index
            for k,n in graph.nodes.items(): #k neighbor id, n its index
                if not drawnList[k]:
                    if Start:
                        nextID = k
                        dir = 90
                        dist = 0
                        Start = False
                        break
                    else:
                        if graph.nodes[this.currentID].isNeighbor(n):
                            nextID = k
                            dir = graph.nodes[this.currentID].getNeighborDirection(n)
                            dist = graph.nodes[this.currentID].getNeighborDistance(n)
                            break
            # do we have an upward triangle?
            upward[nextID] = (graph.nodes[nextID].getDirectionDistance(60)==1) or (graph.nodes[nextID].getDirectionDistance(180)==1) or (graph.nodes[nextID].getDirectionDistance(300)==1)
            # updirection is 0 degree, hence we invert sin and cos
            samplePoint = [samplePoint[0] + np.sqrt(3)/3*this.length*np.sin(dir/180.0*np.pi)*dist,samplePoint[1] + np.sqrt(3)/3*this.length*np.cos(dir/180.0*np.pi)*dist]
            b = graph.nodes[nextID].getColor();
            this.triangleAt(pos=(samplePoint[0],samplePoint[1]),dir=90,length=this.length,fill=(np.asscalar(b[0]),np.asscalar(b[1]),np.asscalar(b[2])),clockwise = (not upward[nextID]))
            this.currentID = nextID
            drawnList[this.currentID] = True
            finished = True
            for k in drawnList.keys():
                finished = finished & drawnList[k]
        t.update()
        time.sleep(1/this.parameters["framerate"])

class PyMatplotSLV(SLV):

    def __init__(this,length=30,limits=[-300,300,-300,300],parameters=None):
        """
        PyMatplotSLC() initialize the vizualization using the python matplot lib
        """
        print("""                              ~~~ Stackenlichten ~~~
           Let\'s blink in lichten. But with German stacken and blochen AND matplot!
                                                                    @kellertuer
        Moin.""")
        super(PyMatplotSLV,this).__init__(parameters)
        this.length=length;
        this.fig = plt.figure()
        this.ax = this.fig.gca()
        this.fig.canvas.mpl_connect("close_event",lambda:sys.exit())
        this.ax.set_xlim([limits[0], limits[1]])
        this.ax.set_ylim([limits[2], limits[3]])
        this.ax.xaxis.set_visible(False)
        this.ax.yaxis.set_visible(False)
        plt.ioff()
        this.patches = []

    def has_been_closed(this):
        fig = this.ax.figure.canvas.manager
        active_fig_managers = plt._pylab_helpers.Gcf.figs.values()
        return fig not in active_fig_managers

    def triangleAt(this,pos=(0.0,0.0),dir=90,length=15,fill=(1.0,1.0,1.0)):
        height = np.sqrt(3)/6*length
        base = [pos[0] + np.sin(dir/180.0*np.pi+np.pi/2.0)*height, pos[1] + np.cos(dir/180.0*np.pi + np.pi/2.0)*height]
        firstP = [base[0] + np.sin(dir/180.0*np.pi)*this.length/2, base[1] + np.cos(dir/180.0*np.pi)*this.length/2]
        secondP = [base[0] - np.sin(dir/180.0*np.pi+np.pi/2)*3.0*height, base[1] - np.cos(dir/180.0*np.pi+np.pi/2)*3.0*height]
        thirdP = [base[0] - np.sin(dir/180.0*np.pi)*this.length/2, base[1] - np.cos(dir/180.0*np.pi)*this.length/2]
        this.patches.append( plt.Polygon([firstP,thirdP,secondP],fill=True,color=fill) )

    def render(this,graph):
        this.ax.cla();
        this.patches = []
        finished = False
        drawnList = dict()
        positions = dict()
        upward = dict()
        for k in graph.nodes.keys():
            drawnList[k] = False
        Start = True
        startPoint = [0.0,0.0]
        while not finished:
            # look for next index
            for k,n in graph.nodes.items(): #k neighbor id, n its index
                if not drawnList[k]:
                    if Start:
                        nextID = k
                        dir = 90
                        dist = 0
                        break
                    else:
                        found=False
                        for k2 in drawnList.keys():
                            if drawnList[k2]:
                                if graph.nodes[k2].isNeighbor(n):
                                    nextID = k
                                    dir = graph.nodes[k2].getNeighborDirection(n)
                                    dist = graph.nodes[k2].getNeighborDistance(n)
                                    samplePoint = positions[k2]
                                    found=True
                                    break
                        if found:
                            break
            # do we have an upward triangle?
            upward[nextID] = (graph.nodes[nextID].getDirectionDistance(60)==1) or (graph.nodes[nextID].getDirectionDistance(180)==1) or (graph.nodes[nextID].getDirectionDistance(300)==1)
            if Start:
                Start = False
                positions[nextID] = startPoint
            else:
                # updirection is 0 degree, hence we invert sin and cos
                positions[nextID] = [samplePoint[0] + np.sqrt(3)/3*this.length*np.sin(dir/180.0*np.pi)*dist,samplePoint[1] + np.sqrt(3)/3*this.length*np.cos(dir/180.0*np.pi)*dist]
            b = graph.nodes[nextID].getColor();
            thisP = positions[nextID]
            if upward[nextID]:
                this.triangleAt(pos=(thisP[0],thisP[1]),dir=90,length=this.length,fill=(b[0],b[1],b[2]))
            else:
                this.triangleAt(pos=(thisP[0],thisP[1]),dir=270,length=this.length,fill=(b[0],b[1],b[2]))
            drawnList[nextID] = True
            finished = True
            for k in drawnList.keys():
                finished = finished & drawnList[k]
        if this.has_been_closed():
            sys.exit()
        this.ax.add_collection(mpc.PatchCollection(this.patches,match_original=True))
        plt.draw()
        plt.pause(1/this.parameters["framerate"])

class PyGameSLV(SLV):

    def __init__(this,length=30,limits=[-300,300,-300,300],parameters=None):
        """
        PyGameSLC() initialize the vizualization using the python matplot lib
        """
        print("""                              ~~~ Stackenlichten ~~~
           Let\'s blink in lichten. But with German stacken and blochen AND matplot!
                                                                    @kellertuer
        Moin.""")
        super(PyGameSLV,this).__init__(parameters)
        this.length=length;
        pygame.init()
        this.screen = pygame.display.set_mode( (limits[1]-limits[0],limits[3]-limits[2]))
        this.limits = limits;
        this.clock = pygame.time.Clock()
        this.screen.fill( (0,0,0) )
        pygame.display.update()

    def has_been_closed(this):
        pygame.quite()

    def triangleAt(this,pos=(0.0,0.0),dir=90,length=15,fill=(1.0,1.0,1.0)):
        #pos = pos + (-this.limits[0],this.limits[2])
        height = np.sqrt(3)/6*length
        base = [pos[0] + np.sin(dir/180.0*np.pi+np.pi/2.0)*height, pos[1] + np.cos(dir/180.0*np.pi + np.pi/2.0)*height]
        firstP = [base[0] + np.sin(dir/180.0*np.pi)*this.length/2, base[1] + np.cos(dir/180.0*np.pi)*this.length/2]
        secondP = [base[0] - np.sin(dir/180.0*np.pi+np.pi/2)*3.0*height, base[1] - np.cos(dir/180.0*np.pi+np.pi/2)*3.0*height]
        thirdP = [base[0] - np.sin(dir/180.0*np.pi)*this.length/2, base[1] - np.cos(dir/180.0*np.pi)*this.length/2]
        f2 = tuple([int(round(255*x)) for x in fill])
        flipud = [[x+length,this.limits[3]-this.limits[2]-y-height] for [x,y] in [firstP,thirdP,secondP]]
        pygame.draw.polygon(this.screen,f2,flipud,0)

    def render(this,graph):
        finished = False
        drawnList = dict()
        positions = dict()
        upward = dict()
        for k in graph.nodes.keys():
            drawnList[k] = False
        Start = True
        startPoint = [0.0,0.0]
        # clear
        this.screen.fill( (0,0,0) )
        while not finished:
            # look for next index
            for k,n in graph.nodes.items(): #k neighbor id, n its index
                if not drawnList[k]:
                    if Start:
                        nextID = k
                        dir = 90
                        dist = 0
                        break
                    else:
                        found=False
                        for k2 in drawnList.keys():
                            if drawnList[k2]:
                                if graph.nodes[k2].isNeighbor(n):
                                    nextID = k
                                    dir = graph.nodes[k2].getNeighborDirection(n)
                                    dist = graph.nodes[k2].getNeighborDistance(n)
                                    samplePoint = positions[k2]
                                    found=True
                                    break
                        if found:
                            break
            # do we have an upward triangle?
            upward[nextID] = (graph.nodes[nextID].getDirectionDistance(60)==1) or (graph.nodes[nextID].getDirectionDistance(180)==1) or (graph.nodes[nextID].getDirectionDistance(300)==1)
            if Start:
                Start = False
                positions[nextID] = startPoint
            else:
                # updirection is 0 degree, hence we invert sin and cos
                positions[nextID] = [samplePoint[0] + np.sqrt(3)/3*this.length*np.sin(dir/180.0*np.pi)*dist,samplePoint[1] + np.sqrt(3)/3*this.length*np.cos(dir/180.0*np.pi)*dist]
            b = graph.nodes[nextID].getColor();
            thisP = positions[nextID]
            if upward[nextID]:
                this.triangleAt(pos=(thisP[0],thisP[1]),dir=90,length=this.length,fill=(b[0],b[1],b[2]))
            else:
                this.triangleAt(pos=(thisP[0],thisP[1]),dir=270,length=this.length,fill=(b[0],b[1],b[2]))
            drawnList[nextID] = True
            finished = True
            for k in drawnList.keys():
                finished = finished & drawnList[k]
        #t = this.clock.tick(this.parameters["framerate"])
        pygame.display.update()
        time.sleep(1/this.parameters["framerate"])
