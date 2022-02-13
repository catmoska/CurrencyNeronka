from neronka import *
import time

i = contolModel(1)
o1y = []
o2y = []
o3y = []
for y in range(20):
    print(y)
    # i.startObusenia(0)
    o1 = i.generitModelMatematek(60)
    o1y.append(o1)
    print(o1)
    # i.startObusenia(0)
    time.sleep(60)
    o2 = i.znaceniaDyblicat()
    print(o2)
    print(o1 - o2)
    o2y.append(o2)
    o3y.append(o1-o2)

print(o1y)
print(o2y)
print(o3y)
print(sum(o3y)/20)
