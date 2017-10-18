from opc import Client        # Der OPC Client
import time
from numpy.random import randint
c = Client('localhost:7890')  # Verbinden
c.set_interpolation(False);   # direkt Setzen
data = [ [0,0,0] ] * 512      # leeres Bild
i=randint(128)                # i-te LED mit
data[i] = randint(256,size=3) # Zufallsfarbe
print(str(i)+':'+str(data[i]))
c.put_pixels(data)            # Farbe setzen
time.sleep(3)                 # 3 Sek. warten
data[i] = [0]*3
c.put_pixels(data)            # und wieder aus
