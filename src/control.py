#!/usr/bin/env python3
from algorithm import *
import time
import curses

def abstractmethod(method):
    def default_abstract_method(*args, **kwargs):
        raise NotImplementedError('call to abstract method ' + repr(method))

    default_abstract_method.__name__ = method.__name__
    
    return default_abstract_method

class Control:
    # standard parameters
    PARAMETERS = {'framerate': 40}
    
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
            
class DirectionControl(Control):
    def __init__(this,algorithm,parameters=None):
        super(DirectionControl,this).__init__(algorithm,parameters)
        this.stdscr = curses.initscr()
        curses.cbreak()
        this.stdscr.keypad(1)
        this.stdscr.nodelay(1)
        
    
    def start(this):
        key = ''
        while not this.algorithm.isFinished():
#            print(this.algorithm.getParameter("Alive"))
            key = this.stdscr.getch()
            dir = None
            if key == ord('f'):
                #print("90",end='',flush=True)
                dir=90
            elif key==ord('r'):
                #print("30",end='',flush=True)
                dir=30
            elif key==ord('e'):
                #print("330",end='',flush=True)
                dir=330
            elif key==ord('d'):
                #print("270",end='',flush=True)
                dir=270
            elif key==ord('x'):
                #print("210",end='',flush=True)
                dir=210
            elif key==ord('c'):
                #print("150",end='',flush=True)
                dir=150
            elif key == ord('q'):
                this.algorithm = mainAlgorithm(this.algorithm.SLC,AlgFadeOut(3*this.PARAMETERS['framerate'],this.algorithm))
                print('o', end='', flush=True)
                while not this.algorithm.isFinished():
                    this.algorithm.step()
                    time.sleep(1/this.parameters["framerate"])
                    print('.', end='', flush=True)
                break;
            if dir is not None:
                this.algorithm.setParameter("Direction",dir)
            # step
            this.algorithm.step()
            time.sleep(1/this.parameters["framerate"])
            print('.', end='', flush=True)
        curses.endwin()
        print("\n\nKthxbye.")
        