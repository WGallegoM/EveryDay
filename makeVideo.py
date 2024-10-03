import numpy as np
import cv2
from pathlib import Path
import re

#TODO organizar fotos a la hora de hacer el video

ROOT_PATH = '/home/willgm/STUFF/Media/evry day photo/'
YEARS = [
    '2021/',
    '2022/',
    '2023/'
    #'2024/'
]

MONTHS = [
    '01 - Enero',
    '02 - Febrero',
    '03 - Marzo',
    '04 - Abril',
    '05 - Mayo',
    '06 - Junio',
    '07 - Julio',
    '08 - Agosto',
    '09 - Septiembre',
    '10 - Octubre',
    '11 - Noviembre',
    '12 - Diciembre'
]

listImages = []

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc, 24.0, (1440,1080))

for im in listImages:
    frame = cv2.imread(ROOT_PATH + im + '.jpg')
    out.write(frame)

for year in YEARS:
    mth_list = []
    print("\nPROCESANDO {} ...\m".format(year))
    for mth in MONTHS:
        print("\nPROCESANDO {} ...\n".format(mth))
        mthPath = ROOT_PATH + year + mth + '/warped/'
        entries = Path(mthPath)
        for entry in entries.iterdir():
            
            if (entry.suffix != '.jpg') or not(bool(re.search(r'warped$', entry.stem))):
                continue

            print("adding {} to the video".format(entry.stem))

            frame = cv2.imread(str(entry))
            out.write(frame)
            

out.release