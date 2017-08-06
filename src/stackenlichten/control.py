#!/usr/bin/env python3
from .algorithm import Algorithm, mainAlgorithm, AlgFadeOut
import time
import curses

def abstractmethod(method):
    def default_abstract_method(*args, **kwargs):
        raise NotImplementedError('call to abstract method ' + repr(method))

    default_abstract_method.__name__ = method.__name__

    return default_abstract_method

class Control:
    """ Control – a controller for the algorithms and hence a graph state
        to be displayed.
    """
    # standard parameters
    PARAMETERS = {'framerate': 50}

    def __init__(this,algorithm,parameters=None):
        this.algorithm = algorithm
        this.parameters = Control.PARAMETERS
        this.observers = []
        if parameters is not None:
            this.parameters = Control.PARAMETERS.copy()
            this.parameters.update(parameters)

    @abstractmethod
    def start(this):
        "start the algorithm as long as its running."
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
        cnt=0
        while not this.algorithm.isFinished():
            cnt=cnt+1
            key = this.stdscr.getch()
            dir = None
            rot = None
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
            elif key==ord('k'):
                rot=-60
            elif key==ord('l'):
                rot=60
            elif key == ord(' '):
                this.update_observers({'EndDisplayDigit':True})
            elif key == ord('q'):
                this.algorithm = mainAlgorithm(this.algorithm.SLC,AlgFadeOut(3*this.PARAMETERS['framerate'],this.algorithm))
                print('o', end='', flush=True)
                while not this.algorithm.isFinished():
                    this.algorithm.step()
                    time.sleep(1/this.parameters["framerate"])
                    print('.', end='', flush=True)
                break;
            if dir is not None:
                this.update_observers({'Direction':dir})
            if rot is not None:
                this.update_observers({'Rotate':rot})
            # step
            this.algorithm.step()
            time.sleep(1/this.parameters["framerate"])
            print('.', end='', flush=True)
            if cnt%this.parameters["framerate"]==0:
                this.stdscr.clear()
                this.stdscr.refresh()
        curses.endwin()
        print("\n\nKthxbye.")
