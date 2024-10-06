import cv2
import re
import config
from pathlib import Path

NAME = config.NAME
FPS = config.FPS
RESOLUTION = config.RESOLUTION
MONTH_EXPRESSION = config.month_expression
ROOT_PATH = config.ROOT_FOLDER_PATH
TEXT = config.TEXT
COLOR_TEXT = config.COLOR_TEXT
FONT = cv2.FONT_HERSHEY_SIMPLEX 

YEARS = [
    '2021/',
    '2022/',
    '2023/',
    '2024/'
]

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(NAME + '.avi',fourcc, FPS, RESOLUTION)

number_photos = 0

COLOR_TEXT = (COLOR_TEXT[2] , COLOR_TEXT[1], COLOR_TEXT[0]) # cambia el color de RGB a BGR

for year in YEARS:
    Path_year = Path(ROOT_PATH + year)
    monthsAvalible = [x.stem for x in Path_year.iterdir() if (x.is_dir() and re.match(MONTH_EXPRESSION,x.stem))] #agrega a una lista solo los nombres de las carpetas que tengan la forma y nombre de un mes
    monthsAvalible.sort()

    print("\nPROCESANDO {} ...\m".format(year))

    for mth in monthsAvalible:
        print("\nPROCESANDO {} ...\n".format(mth))
        mthPath = ROOT_PATH + year + mth + '/warped/'
        entries = Path(mthPath)

        if not(entries.exists()): # si la carpeta warped no existe se salta el mes
            print(r'there is no "warped" folder for this month')
            continue 
        
        sortedEntries = sorted(entries.iterdir())
        for entry in sortedEntries:
            if (entry.suffix != '.jpg') or not(bool(re.search(r'warped$', entry.stem))):
                continue
            number_photos += 1

            print("adding pic #{} {} to the video {}".format(str(number_photos),entry.stem,NAME))

            frame = cv2.imread(str(entry))

            if TEXT:
                cv2.putText(frame,  
                entry.stem,  
                (RESOLUTION[0] - 200 , RESOLUTION[1] - 30),  
                FONT, 1,  
                COLOR_TEXT,  # el color esta en BGR
                2,  
                cv2.LINE_4,
                ) 

            out.write(frame)
            

out.release