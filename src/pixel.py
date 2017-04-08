import math

class Pixel:
    'A pixel class including its neighbors'
    ID = 0
    color = [0,0,0]
    neighbor = []
    neighborDirection = []
    nbeighborDistance = []
    brightness = 1.0
    
    def __init__(this, ID, neighbor = [], neighborDirection = [], neighborDistance = [], color = [0,0,0]):
        'initialize pixel with a color and its neighbors'
        this.ID = ID
        this.color = color
        this.neighbor = neighbor
        if len(neighborDirection) == 0:
            num = len(neighbors)
            step = math.floor(360/num)
            this.neighborDirection = [(i+step)%360 for i in  range(0,360,step)]
        else:
            this.neighborDirection = neighborDirection
        if len(neighborDistance) == 0:
            this.neighborDistance = len(this.neighbor)*[1]
        else:
            this.neighborDistance = neighborDistance

    def __repr__(this):
        neighborStrings = ''
        for idS, dirS, distS in zip(this.neighbor, this.neighborDirection, this.neighborDistance):
            neighborStrings += '(#'+str(idS)+' '+str(dirS)+':'+str(distS)+') '
        neighborStrings = neighborStrings[:-1] #remove last string
        return '#'+str(this.ID)+' with neighbors '+neighborStrings
        
    def dimm(this,brightness):
        'Dim this pixel down to brightness, which is a value between 1 (full brightness) and 0 (off) '
        this.brightness = max(min(brightness,1),0)
        
    def setColor(this,color, brightness=1.0):
        'set color to a value and reset brightness'
        this.color = color
        this.brightness = brightness

    def getColor(this):
        return [i*this.brightness for i in this.color]