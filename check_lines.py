content = open('D:/HarvestHand/run_crossval.py').read().split('\n')
for i in range(148, 168):
    print(f'{i+1}: [{content[i]}]')