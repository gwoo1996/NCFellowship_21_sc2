import math

min_units = list()
min_units.append(1)
min_units.append(2)
print(len(min_units))
print(min_units)
min_units.pop(0)
print(min_units)
print(min_units[0])
min_units.pop(0)
print('start min_units')
print(min_units)
for i in range (1,1000):
    for i in range(1,1000):
        min_units.append(i)

    for i in range(1,1000):
        min_units.pop(0)
        
    for i in range(1,1000):
        min_units.append(i)

    for i in range(1,1000):
        min_units.pop(0)


print('after pop')
print(min_units)

if len(min_units) > 0:
    print('yureka')

