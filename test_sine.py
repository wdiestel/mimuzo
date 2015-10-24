import time
from i_sine import Sine

s = Sine(3,3)

s.play(1,2,1.0)
time.sleep(1)
s.play(2,2,1.0)
time.sleep(1.5)
s.play(2,0,1.0)
