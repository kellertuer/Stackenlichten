import includes.opc as opc
import numpy as np
from graph import Graph

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
            v = [i*scale*this.MAX_BRIGHTNESS for i in graph.nodes[k].getColor()]
            if k > 512:
                 raise ValueError("The graph node id " + str(k) * " is too large for the fadecandy board (max 512 LEDs).\nPlease reorder or reduce the number")
            data[k-1] = tuple( np.round(v) )
        this.client.put_pixels(data)
