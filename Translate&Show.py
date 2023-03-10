import cv2
import deep_translator.exceptions
import pytesseract
from deep_translator import GoogleTranslator, single_detection
import detectlanguage

detect_language_api='7f2eddfd7b8fb4ad03628fbedbfb5aae'

pytesseract.pytesseract.tesseract_cmd ='C:/Program Files/Tesseract-OCR/tesseract.exe'
img=cv2.imread('assets/tam.png')
img=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


boxes = pytesseract.image_to_data(img)
hTmg, wImg, _ = img.shape

for x, b in enumerate(boxes.splitlines()):
    if x != 0:
        b = b.split()
        # print(b)
        if len(b) == 12:
            x,y,w,h = int(b[6]), int(b[7]), int(b[8]), int(b[9])
            cv2.rectangle(img, (x,y), (w+x,h+y), (0,0,255), 1)
            text = b[11]
            try:
                lang = single_detection(text, api_key=detect_language_api)
                try:
                    translated_text = GoogleTranslator(source='auto', target='english').translate_file('test.txt')
                    cv2.putText(img, translated_text, (x,y), cv2.FONT_HERSHEY_COMPLEX, 1, (50,50,255), 2)
                except deep_translator.exceptions.InvalidSourceOrTargetLanguage:
                    cv2.putText(img, text, (x,y), cv2.FONT_HERSHEY_COMPLEX, 1, (50,50,255), 1)
            except IndexError:
                cv2.putText(img, text, (x,y), cv2.FONT_HERSHEY_COMPLEX, 1, (50,50,255), 1)

# print(lang)
# print(text)
cv2.imshow('RESULT', img)
cv2.waitKey(0)
cv2.destroyAllWindows()