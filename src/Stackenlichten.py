import includes.opc as opc
import numpy as np
from graph import Graph
import turtle as t

def abstractmethod(method):
    def default_abstract_method(*args, **kwargs):
        raise NotImplementedError('call to abstract method ' + repr(method))

    default_abstract_method.__name__ = method.__name__
    
    return default_abstract_method

class SLC:
    "StackenLichtenControl - the connector to the USB board"

    MAX_BRIGHTNESS = 255
    
    @abstractmethod
    def render(this, graph,scale=1):
        "render(graph) – renders a graph onto the Stackenlichten and activates the LEDs."
        pass
        
class FadecandySLC(SLC):
    client = None

    def __init__(this,url='localhost:7890'):
        """
        FadecandySLC() initializes the Open Pixel Control (OPC) to connect to
        the usual localhost fadecandy server.
        """
        print("""                              ~~~ Stackenlichten ~~~                            
           Let\'s blink in lichten. But with German stacken and blochen.         
                                                                     @kellertuer
Moin.""")
        this.client = opc.Client(url)

    def render(this, graph,scale=1):
        data = [ (0,0,0) ] * 512
        for k in graph.nodes.keys():
            v = [i*scale*this.MAX_BRIGHTNESS*graph.nodes[k].brightness for i in graph.nodes[k].getColor()]
            if k > 512:
                 raise ValueError("The graph node id " + str(k) * " is too large for the fadecandy board (max 512 LEDs).\nPlease reorder or reduce the number")
            data[k-1] = tuple( np.round(v) )
        this.client.put_pixels(data)

class PyTurtleSLC():
    
    def __init__(this,length=30):
        """
        PyTurtleSLC() initialize the vizualization using the python turtle module
        """
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
            this.triangleAt(pos=(samplePoint[0],samplePoint[1]),dir=90,length=this.length,fill=graph.nodes[nextID].getColor(),clockwise = (not upward[nextID]))
            this.currentID = nextID
            drawnList[this.currentID] = True
            finished = True
            for k in drawnList.keys():
                finished = finished & drawnList[k]
        t.update()
