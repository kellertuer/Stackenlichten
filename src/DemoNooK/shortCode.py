from opc import Client
import time
c = Client('localhost:7890')
c.set_interpolation(False)
data = [ (0,0,0) ] * 512
for j in (32,64,128):
    for i in range(0,128):
        data[i] = (255-j,j,2*j)
        c.put_pixels(data)
        time.sleep(0.5/j)
        data[i] = (0,0,0)
# Turn off again
c.put_pixels(data)
