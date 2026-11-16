import os
path = 'D:/HarvestHand/output.txt'
if os.path.exists(path):
    size = os.path.getsize(path)
    print('File size:', size)
    with open(path, 'r') as f:
        content = f.read()
        print('Last 500 chars:')
        print(content[-500:])
else:
    print('File not found')
