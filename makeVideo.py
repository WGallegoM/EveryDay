import numpy as np
import cv2
from pathlib import Path
import re

root = '/home/willgm/STUFF/Media/evry day photo/'
years = [
    '2024'
]

months = [
    '01 - Enero',
    '02 - Febrero',
    '03 - Marzo',
    '04 - Abril',
    '05 - Mayo',
    '06 - Junio',
    '07 - Julio',
    '08 - Agosto',
    '09 - Septiembre'
]
listImages = []

entries = Path(root)
for entry in entries.iterdir():
    
    if (entry.suffix != '.jpg') or not(bool(re.search(r'warped$', entry.stem))):
        continue
        
    listImages.append(entry.stem)

listImages.sort()

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc, 2.0, (1440,1080))

for im in listImages:
    frame = cv2.imread(root + im + '.jpg')
    out.write(frame)

out.release