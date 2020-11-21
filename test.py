import os
import glob

path = os.path.dirname(__file__) + '/icons/cute_anims'
files = []
for r, d, f in os.walk(path):
    for file in f:
        if '.txt' in file:
            files.append(os.path.join(r, file))
print(path)
print(len(files))
for f in files:
    print(f)
