import cv2
import face_recognition
import everydayUtilities as evday
from pathlib import Path

'''CONFIGURACIONES DEL SCRIPT'''
WRITE_BLEND = True #si el valor es TRUE se guarda una imagen que mezcla el source y el objetivo
MODEL_SIZE = "large" #tamaño de los landmarks small/large
SOURCE_IMAGE = '/home/user/Media/evry day photo/sources/19_11_2023_H14-45-21.jpg'
EXTENSION = '.jpg'

MONTHS = [
    '05 - Mayo'
]

for mth in MONTHS:
    print('PROCESANDO {}'.format(mth))
    ROOT_FOLDER = '/home/user/Media/evry day photo/2021/' + mth + '/'
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

    # Carga los rostos que conoce y saca los encodings 
    subject_image = face_recognition.load_image_file("known/subject.jpg")
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
    print('extracting info of the subject in the images...')
    image_info = [evday.get_Subject_Info(im,subject_encoding,modelSize=MODEL_SIZE) for im in images_to_compare] #Array de diccionarios con landmarks y locations

    #output_images = np.empty((numberImages,3000,4000,2),dtype=np.uint8)

    #cambia la imagen source a BGR
    print('changing color of SOURCE')
    source_info['image'] = cv2.cvtColor(source_info['image'], cv2.COLOR_RGB2BGR)

    print('processing images...')
    for i in range(numberImages):
        print('processing image {}'.format(i))
        #cambia la i-esima imagen a BGR
        images_to_compare[i] = cv2.cvtColor(images_to_compare[i], cv2.COLOR_RGB2BGR)
        #Halla la homografia entre las dos fotos
        h, status = cv2.findHomography(image_info[i]['landmarks'],source_info['landmarks'])
        #hace el cambio de perspectiva de la imagen
        im_out = cv2.warpPerspective(images_to_compare[i], h, (source_info['image'].shape[1],source_info['image'].shape[0]))
        #output_images.append(im_out)

        cv2.imwrite(OUTPUT_FOLDER + ImageNames[i] + '-warped' + '.jpg',im_out)

        if WRITE_BLEND:
            cv2.imwrite(OUTPUT_FOLDER + ImageNames[i] + '-blend'  + '.jpg',cv2.addWeighted(im_out,0.6,source_info['image'],0.4,0)) 

print("END")