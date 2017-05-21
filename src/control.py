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
    PARAMETERS = {'framerate': 30}
    
    def __init__(this,algorithm,parameters=None):
        this.algorithm = algorithm
        this.parameters = Control.PARAMETERS
        if parameters is not None:
            this.parameters = Control.PARAMETERS.copy()
            this.parameters.update(parameters)

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
            this.algorithm = mainAlgorithm(this.algorithm.SLC,AlgFadeOut(2*this.PARAMETERS['framerate'],this.algorithm))
            print('o', end='', flush=True)
            while not this.algorithm.isFinished():
                this.algorithm.step()
                time.sleep(1/this.parameters["framerate"])
                print('.', end='', flush=True)
            print("\n\nKthxbye.")