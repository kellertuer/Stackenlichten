#!/usr/bin/env python3
from algorithm import *
import time

def abstractmethod(method):
    def default_abstract_method(*args, **kwargs):
        raise NotImplementedError('call to abstract method ' + repr(method))

    default_abstract_method.__name__ = method.__name__
    
    return default_abstract_method

class Control:
    # standard parameters
    PARAMETERS = {'framerate': 12}
    
    def __init__(this,algorithm,parameters=None):
        this.algorithm = algorithm
        if parameters is not None:
            this.parameters = parameters
        else:
            this.parameters = Control.PARAMETERS
    
    @abstractmethod
    def start(this):
        "start the algorithm as long as its running."
        pass
    
class SimpleControl(Control):
    def __init__(this,algorithm,parameters=None):
        super(SimpleControl,this).__init__(algorithm,parameters)
    
    def start(this):
        try: #Check for Keypresses
            while not this.algorithm.isFinished():
                this.algorithm.step()
                time.sleep(1/this.parameters["framerate"])
                print('.', end='', flush=True)
        except KeyboardInterrupt:
            #set back hard to black
            this.algorithm.setBlack()
            print("\n\nKthxbye.")