import os
content = open('D:/HarvestHand/run_crossval.py').read().split('\n')
for i in range(150, 160):
    print(f'{i+1}: [{content[i]}]')