#evrydayPic Configs
WRITE_BLEND = True #si el valor es TRUE se guarda una imagen que mezcla el source y el objetivo
MODEL_SIZE = "large" #tamaño de los landmarks small/large
SOURCE_IMAGE = '/YourRoute/Media/evry day photo/sources/19_11_2023_H14-45-21.jpg' # imagen de referencia con la que se haran las homografias
ROOT_FOLDER_PATH = '/YourRoute/Media/evry day photo/' #folder donde se encuentran todas las subcarpetas de los años
EXTENSION = '.jpg'

#makeVideo Config
FPS = 12.0 #FPS del video resultante
NAME = "evDayVideo" #Nombre del video output
RESOLUTION = (1440,1080) #resolucion del video output
COLOR_TEXT = (65, 255, 0) #RGB color for the text in video
TEXT = True #en el video se muestra el nombre de la foto
month_expression = r'^\d\d\s-\s(Enero|Febrero|Marzo|Abril|Mayo|Junio|Julio|Agosto|Septiembre|Octubre|Noviembre|Diciembre)' #expresion REGEX que valida los nombres de las carpetas de los años