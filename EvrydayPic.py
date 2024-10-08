import cv2
import face_recognition
import everydayUtilities as evday
import config
from pathlib import Path

'''CONFIGURACIONES DEL SCRIPT'''
WRITE_BLEND = config.WRITE_BLEND #si el valor es TRUE se guarda una imagen que mezcla el source y el objetivo
MODEL_SIZE = config.MODEL_SIZE #tamaño de los landmarks small/large
SOURCE_IMAGE = config.SOURCE_IMAGE
ROOT_FOLDER_PATH = config.ROOT_FOLDER_PATH
EXTENSION = config.EXTENSION

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
    '12 - Diciembre',
]

for mth in MONTHS:
    print('PROCESANDO {}'.format(mth))
    ROOT_FOLDER = ROOT_FOLDER_PATH + mth + '/'
    OUTPUT_FOLDER = ROOT_FOLDER + 'warped/'

    #Imagenes a comparar
    ImageNames= []
    numberImages = 0

    entries = Path(ROOT_FOLDER)
    for entry in entries.iterdir():
        if entry.suffix != '.jpg':
            continue

        ImageNames.append(entry.stem)
        numberImages += 1

    ImageNames.sort()

    # Carga los rostos que conoce y saca los encodings 
    subject_image = face_recognition.load_image_file(SOURCE_IMAGE)
    subject_encoding = face_recognition.face_encodings(subject_image)[0]

    knownFaces = [
        subject_encoding,
        ]

    known_names=[
        "subject",
    ]

    #toma la info de subject en la imagen SOURCE
    source_info ={'image':face_recognition.load_image_file(SOURCE_IMAGE)}

    for key,value in evday.get_Subject_Info(source_info['image'],subject_encoding,modelSize=MODEL_SIZE).items():
        source_info[key] = value

    '''En la linea 56 se cargan las imagenes en un array, mientras que en la 
    linea 58 se crea un array cuya i-esima entrada guarda un diccionario
    con los las landmarks y locations del subject en esa imagen'''
    print('Loading images...')
    images_to_compare = [face_recognition.load_image_file(ROOT_FOLDER + imName + EXTENSION) for imName in ImageNames] #Array de imagenes

    #output_images = np.empty((numberImages,3000,4000,2),dtype=np.uint8)

    image_info = [None for i in range(numberImages)] #declaracion de image info

    #cambia la imagen source a BGR
    print('changing color of SOURCE')
    source_info['image'] = cv2.cvtColor(source_info['image'], cv2.COLOR_RGB2BGR)

    print('processing images...')
    for i in range(numberImages):
        print('processing image {0} -> {1}'.format(i,str(ImageNames[i]) ) )
        image_info[i] = evday.get_Subject_Info(images_to_compare[i],subject_encoding,modelSize=MODEL_SIZE) #Array de diccionarios con landmarks y locations
        
        if (image_info[i] == None):
            print("No se pudo encontrar al subject en la imagen {0} -> {1}".format(i,str(ImageNames[i])))            
            continue
        #cambia la i-esima imagen a BGR
        images_to_compare[i] = cv2.cvtColor(images_to_compare[i], cv2.COLOR_RGB2BGR)
        #Halla la homografia entre las dos fotos
        h, status = cv2.findHomography(image_info[i]['landmarks'],source_info['landmarks'])
        #hace el cambio de perspectiva de la imagen
        im_out = cv2.warpPerspective(images_to_compare[i], h, (source_info['image'].shape[1],source_info['image'].shape[0]))

        cv2.imwrite(OUTPUT_FOLDER + ImageNames[i] + '-warped' + '.jpg',im_out)

        if WRITE_BLEND:
            cv2.imwrite(OUTPUT_FOLDER + ImageNames[i] + '-blend'  + '.jpg',cv2.addWeighted(im_out,0.6,source_info['image'],0.4,0)) 

print("END")