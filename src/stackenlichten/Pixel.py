import math

class Pixel:
    'A pixel class including its neighbors'
    ID = 0
    color = [0,0,0]
    neighborDirection = {}
    nbeighborDistance = {}
    brightness = 1.0

    def __init__(this, ID, neighborDirection = {}, neighborDistance = {}, color = [0,0,0]):
        'initialize pixel with a color and its neighbors'
        this.ID = ID
        this.color = color
        if len(neighborDistance) == 0 and len(neighborDistance) == 0:
            raise ValueError("At least one of the dictionaries of Directions or Distances has to be provied")
        this.neighborDirection = neighborDirection
        if len(this.neighborDirection) == 0:
            dir = 0;
            dirStep = 360/len(neighborDistance)
            for k in neighborDistance.keys():
                this.neighborDirection[k] = dir
                dir += dirStep
        this.neighborDistance = neighborDistance
        if len(this.neighborDistance) == 0:
            for k in this.neighborDirection.keys():
                this.neighborDistance[k] = 1

    def __repr__(this):
        neighborStrings = ''
        for  k in this.neighborDirection.keys():
            neighborStrings += '(#'+str(k)+' '+str(this.neighborDirection[k])+':'+str(this.neighborDistance[k])+') '
        neighborStrings = neighborStrings[:-1] #remove last string
        return '#'+str(this.ID)+' ['+str(this.color[0])+','+str(this.color[1])+','+str(this.color[2])+'] with neighbors '+neighborStrings

    def dimm(this,brightness):
        'Dim this pixel down to brightness, which is a value between 1 (full brightness) and 0 (off) '
        this.brightness = max(min(brightness,1),0)

    def setColor(this,color, brightness=1.0):
        'set color to a value and reset brightness'
        this.color = color
        this.brightness = brightness
    def getColor(this):
        return [i*this.brightness for i in this.color]
    def addToColor(this,color):
        this.color = [max(min(this.color[i]+color[i],1.0),0) for i in range(3)]

    def isNeighbor(this,pixel):
        return pixel.ID in this.neighborDirection.keys()

    def addNeighbor(this,pixel,direction,distance):
        this.neighborDirection[pixel.ID] = direction
        this.neighborDistance[pixel.ID] = distance

    def removeNeighbor(this,pixel):
        if this.isNeighbor(pixel):
            this.neighborDirection.pop(pixel.ID)
            this.neighborDistance.pop(pixel.ID)

    def getNeighborDirection(this,pixel):
        if pixel.ID in this.neighborDirection.keys():
            return this.neighborDirection[pixel.ID]
        else:
            None

    def getNeighborDistance(this,pixel):
        if pixel.ID in this.neighborDistance.keys():
            return this.neighborDistance[pixel.ID]
        else:
            None

    def getNeighborIDs(this):
        return list(this.neighborDistance.keys())

    def getDirectionDistance(this,direction):
        "get the Distance a pixel is at in given direction"
        for k in this.neighborDirection.keys():
            if this.neighborDirection[k]  == direction:
                return this.neighborDistance[k]
        return None

    def getDirectionNeighborID(this,direction):
        "get the ID of a pixel is at in given direction"
        for k in this.neighborDirection.keys():
            if this.neighborDirection[k]  == direction:
                return k
        return None

    def clone(this):
        p = Pixel(this.ID,this.neighborDirection,this.neighborDistance,this.color)
        p.brightness = this.brightness
        return p
    def __add__(this,pixel):
        color = [min(this.color[i]+pixel.color[i],1.0) for i in range(3)]
        brightness = min(this.brightness+pixel.brightness,1.0)
        p = Pixel(this.ID,this.neighborDirection,this.neighborDistance,color)
        p.brightness = brightness;
        return p
    def __iadd__(this,pixel):
        this.color = [min(this.color[i]+pixel.color[i],1.0) for i in range(3)]
        this.brightness = min(this.brightness+pixel.brightness,1.0)
        return this
    def __radd__(this,pixel):
        return this+pixel
    def __mul__(this,pixel):
        color = [min(this.color[i]*pixel.color[i],1.0) for i in range(3)]
        brightness = min(this.brightness*pixel.brightness,1.0)
        p = Pixel(this.ID,this.neighborDirection,this.neighborDistance,color)
        p.brightness = brightness;
        return p
    def __imul__(this,pixel):
        this.color = [min(this.color[i]*pixel.color[i],1.0) for i in range(3)]
        this.brightness = min(this.brightness*pixel.brightness,1.0)
        return this
