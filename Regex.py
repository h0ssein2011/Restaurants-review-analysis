import re

# read the file
with open('aspects.txt', 'r') as f:
    aspects = [i.rstrip() for i in f.readlines() ]
    f.close()
print(aspects)
print('total number of aspects: ',len(aspects))

