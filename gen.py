from zuid import ZUID

import time


for b in range(10, 33):
    gen = ZUID(prefix='lero_', bytelength=b, timestamped=True)
    m, d = gen.collision_probability()


gen = ZUID(prefix='lero_')
while 1:
    v = gen()

    print(v, len(v))

    #time.sleep(0.1)
