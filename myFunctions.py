from PIL import Image, ImageDraw
import numpy as np

'''funciones utilizadas para experimentar y hacer debugging'''

def circleWithPoint(drawObject, point, rad, F = None, OT = None, W = 1):
    drawObject.rounded_rectangle([point, (point[0] + rad,point[1] + rad)], radius=rad/2, fill=F, outline=OT, width=W)
    return None

def dictTolengts(myDict):
    newDict = {}
    for keys in myDict:
        newDict[keys] = len(myDict[keys])

    return newDict

def countTrues(myArr):
    result = 0
    for value in myArr:
        if value:
            result += 1

    return result

def trueIndex_and_count(myArr):
    result = 0
    index= []

    for i in range(len(myArr)):
        if myArr[i]:
            result += 1
            index.append(i)

    return (index,result)
