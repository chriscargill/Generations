from random import *

x = "01"
y = "01"
x1 = 1
y1 = 1

myfile = open('lines', 'a')
for number in range(1,10): 
    myfile.write(f'"{x}{y}":(sectionW*{x1}, sectionH*{y1}),\n')
    tx = int(x)+1
    if tx < 10:
        newX = str(0) + str(tx)
        x = newX
    else:
        newX = str(tx)
        x = newX


    tx1 = x1+1
    x1 = tx1
myfile.close()