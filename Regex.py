import re

# read the file
with open('aspects.txt', 'r') as f:
    aspects = f.readlines()

print(aspects)
print('total number of aspects: ',len(aspects))

