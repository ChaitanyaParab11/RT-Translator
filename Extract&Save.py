import cv2
import easyocr
import matplotlib.pyplot as plt
from pylab import rcParams
from IPython.display import Image
import numpy as np
# from PIL import Image
lang=['ta']
reader = easyocr.Reader(lang, gpu=False)

vid = cv2.VideoCapture(0)
while (True):

    ret, frame = vid.read()
    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

output = reader.readtext(frame, paragraph='False')

deftext = output[0][1]

print(output)
print(deftext)

file=open("Python/test.txt", "w", encoding="utf-8")
rt = file.write(deftext)
file.close()
print(rt)