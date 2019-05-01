from zuid import ZUID

import time


gen = ZUID(prefix='lero_', bytelength=16, timestamped=True)
print(gen.collision_probability())

while 1:
    v = gen()

    print(v, len(v))

    #time.sleep(0.1)
