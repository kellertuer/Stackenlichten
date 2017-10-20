from opc import Client
import time
from numpy.random import randint
c = Client('localhost:7890')
c.set_interpolation(False)
data = [ (0,0,0) ] * 512
listA = range(0,100);
listB = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,
    18,20,21,51,50,52,53,75,74,76,77,91,90,92,93,99,98,100,
    98,97,95,96,86,85,83,84,66,65,63,64,38,37,35,36,
    35,34,33,32,31,30,29,28,27,26,25,24,23,22,
    23,49,48,54,55,73,72,78,79,89,88,94,
    88,87,81,82,68,67,61,62,40,39,
    40,41,42,43,44,45,46,47,
    46,56,57,71,70,80,
    70,69,59,60,
    59,58,57,71,70,69] # final circle
listB = [i-1 for i in listB] #shift first led to 0
myList = listB + list(reversed(listB))
colors = [ (70, 166, 127) ]
times = [700]
try:
    while True:
        for k in colors:
            for j in times:
                for i in myList:
                    data[i] = k
                    c.put_pixels(data)
                    time.sleep(1.0/j)
                    data[i] = (0,0,0)
except KeyboardInterrupt:
    # Turn off again
    data = [ (0,0,0) ] * 512
    c.put_pixels(data)
