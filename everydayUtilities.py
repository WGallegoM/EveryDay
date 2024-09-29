import face_recognition
import numpy as np
from PIL import Image,ImageDraw


def getWarpedImage(subject_face,image_to_warp):
    pass

def resize_images_from_folder(folder,size):
    pass

def save_info_from_image(image_name):
      """"saves the landmarks and locations of subject face in
      a txt file"""
      pass

def get_Image_info(image):
     '''toma toda la imagen de la informacion de todos los rostros
     locations,encodings,landmarks'''
     pass

def get_Subject_Index(imageEncodings,subjectEncoding):
      '''Toma como argumentos los encodings de una imagen (un array de numpy)
        y el encoding del rostro de subject. Devuelve el indice del encoding
        más cercano a subject'''
      distances = face_recognition.face_distance(imageEncodings,subjectEncoding)
      return np.argmin(distances)

def DictToPointsNP(myDict):
    '''Pasa el diccionario de landmarks que usa face_recognition
    a un array de numpy para que los puntos puedan ser usados para
    encontrar la homografia'''
    PointList = np.empty((72,2),dtype=np.int64)
    pointNumber = 0
    for Keys in myDict:
        for point in myDict[Keys]:
            PointList[pointNumber] = point
            pointNumber +=1

    return PointList

def get_Subject_Info(image,subjectEncoding,modelSize='large',returnEncoding = False):
    '''Busca en una imagen al subject y entrega informacion como 
    sus landmarks y locations, tambien puede entregar en encoding '''

    '''se toman los locations,encodings y landmarks de 
    cada rostro presente en la imagen'''
    image_locations = face_recognition.face_locations(image)
    image_encodings = face_recognition.face_encodings(image,image_locations)
    image_landmarks = face_recognition.face_landmarks(image,image_locations,model=modelSize)

    if (not image_locations):
        print("no se encontro en subject en la imagen")
        return None
    
    '''se toma el indice del rostro que mejor representa a Subject'''
    subjectIndex = get_Subject_Index(image_encodings,subjectEncoding)

    if returnEncoding:
        return {'landmarks':DictToPointsNP(image_landmarks[subjectIndex]),
                'location':image_locations[subjectIndex],
                'encoding': image_encodings[subjectIndex]}
    else:
        return {'landmarks':DictToPointsNP(image_landmarks[subjectIndex]),
                'location':image_locations[subjectIndex]}

def drawlandmarks(images_to_compare,locations_William,landmarks_William):
    print("Drawing...")
    imageInfo = zip(images_to_compare,locations_William,landmarks_William)
    drawed_images = []
    for im,locations,landmarks in imageInfo:
        
        image_to_draw = Image.fromarray(im)
        draw = ImageDraw.Draw(image_to_draw)

        drawed_images.append(image_to_draw)

        top,right,bottom,left = locations
    
        draw.rectangle(((left, top), (right, bottom)), outline=(0,255,0),width=10)

        for facial_feature in landmarks.keys():
            draw.line(landmarks[facial_feature],fill=(0,255,0) ,width=5)

        # Remove the drawing library from memory as per the Pillow docs
        del draw

        image_to_draw.show()