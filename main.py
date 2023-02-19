# from Take_Trans import *
# from Cam_Trans import *
# from Pdf_Trans import *
# from Text_Trans import * 
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from PyPDF2 import PdfReader
from deep_translator import GoogleTranslator
from translate import Translator
import cv2
import deep_translator.exceptions
import pytesseract
from deep_translator import GoogleTranslator, single_detection
import easyocr
from IPython.display import Image
# from kivy.core.window import Window

abc = "hello"

class SayHello(App):
    def build(self):
        

        #returns a window object with all it's widgets
        # Window.clearcolor = (0,0,0,1)
        self.window = GridLayout()
        self.window.cols = 1
        self.window.size_hint = (0.6, 0.7)
        self.window.pos_hint = {"center_x": 0.5, "center_y":0.5}


        # image widget
        # self.window.add_widget(Image(source='logo.png'))
        def _init_(self,*kwargs):
            self.source='logo.png'
            self.bind(on_load=self.on_image_load)

        def on_image_load(self,*args):
            print("Image Loaded Sucessfully")

        # label widget
        self.greeting = Label(
                        text= "Choose The Language!",
                        font_size= 18,
                        color= '#00FFCE'
                        )
        self.window.add_widget(self.greeting)

        # text input widget
        # self.user = TextInput(
        #             multiline= False,
        #             padding_x= (20,20),
        #             size_hint= (1, 0.5),
        #             )
        
        # # self.user.bind(on_text_validate=on_enter)

        # self.window.add_widget(self.user)

        self.user = TextInput(
            multiline=False,
            padding_x=(20,20),
            size_hint=(1, 0.5),
        )
        self.user.bind(on_text_validate=self.textcallback)
        self.window.add_widget(self.user)


        # selfgreeting = Label(
        #             text='texttranslate(self.user.text)',font_size= 18,
        #                     # pos=(160, 195),
        #                     # size=(500, 55),
        #                     size_hint= (1, 0.5))
        # # with selfgreeting.canvas:
        # #             Color(69,45,23,0.50)
        # #             Rectangle(pos=selfgreeting.pos, size=selfgreeting.size
        # #             )
                        
        # self.window.add_widget(selfgreeting)

        self.greeting = Label(
            text="",
            font_size=18,
            size_hint=(1, 0.5),
        )
        self.window.add_widget(self.greeting)


        # button widget
        self.button = Button(
                      text= "CONVERT",
                      size_hint= (1,0.5),
                      bold= True,
                      background_color ='#00FFCE',
                      #remove darker overlay of background colour
                      # background_normal = ""
                )
                        
        self.button.bind(on_press=self.textcallback)
        self.window.add_widget(self.button)  

        self.button = Button(
                    text= "TAKE IMAGE",
                    size_hint= (1,0.5),
                    bold= True,
                    background_color ='#00FFCE',
                    #remove darker overlay of background colour
                    # background_normal = ""
                )
        self.button.bind(on_press=self.callback)
        self.window.add_widget(self.button)

        self.button = Button(
                    text= "OPEN CAMERA",
                    size_hint= (1,0.5),
                    bold= True,
                    background_color ='#00FFCE',
                    #remove darker overlay of background colourq
                )
        self.button.bind(on_press=self.camcallback)
        self.window.add_widget(self.button)

        self.button = Button(
                    text= "PDF",
                    size_hint= (1,0.5),
                    bold= True,
                    background_color ='#00FFCE',
                    #remove darker overlay of background colourq
                )
        self.button.bind(on_press=self.pdfcallback)
        self.window.add_widget(self.button)

        return self.window


    # def textcallback(self, instance):
    #     # change label text to "Hello + user name!"
    #     # self.greeting.text = "Hello " + self.user.text + "!"
    #     # texttranslate(self.user.text)
    #     lang="German"
    #     translator= Translator(to_lang=lang)
    #     translation = translator.translate(ptext.capitalize())
    #     print(translation)
    #     return translation
    
    def textcallback(self, instance):
        ptext = self.user.text
        lang = "German"
        translator = Translator(to_lang=lang)
        translation = translator.translate(ptext.capitalize())
        self.greeting.text = translation  # update Label text with translation result

    def callback(self, instance):
        # change label text to "Hello + user name!"
        # self.greeting.text = "Hello " + self.user.text + "!"
        detect_language_api='7f2eddfd7b8fb4ad03628fbedbfb5aae'

        lang=['ta']
        reader = easyocr.Reader(lang, gpu=False)

        # vid = cv2.VideoCapture(0)
        # while (True):

        #     ret, frame = vid.read()
        #     cv2.imshow('frame', frame)

        #     if cv2.waitKey(1) & 0xFF == ord('q'):
        #         break
        location = 'assets/download.jpg'
        frame=location

        output = reader.readtext(frame, paragraph='False')

        deftext = output[0][1]

        print(output)
        print(deftext)

        file=open("test.txt", "w", encoding="utf-8")
        rt = file.write(deftext)
        file.close()
        print(rt)

        pytesseract.pytesseract.tesseract_cmd ='C:/Program Files/Tesseract-OCR/tesseract.exe'
        img=cv2.imread(location)
        img=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


        boxes = pytesseract.image_to_data(img)
        hTmg, wImg, _ = img.shape

        for x, b in enumerate(boxes.splitlines()):
            if x != 0:
                b = b.split()
                # print(b)
                if len(b) == 12:
                    x,y,w,h = int(b[6]), int(b[7]), int(b[8]), int(b[9])
                    cv2.rectangle(img, (x,y), (w+x,h+y), (255,0,0), -1)
                    text = b[11]
                    try:
                        lang = single_detection(text, api_key=detect_language_api)
                        try:
                            translated_text = GoogleTranslator(source='auto', target='english').translate_file('test.txt')
                            cv2.putText(img, translated_text, (40,50), cv2.FONT_HERSHEY_COMPLEX,0.7, (255,255,255), 2)
                        except deep_translator.exceptions.InvalidSourceOrTargetLanguage:
                            pass
                            # cv2.putText(img, text, (x,y), cv2.FONT_HERSHEY_COMPLEX, 1, (50,50,255), -1)
                    except IndexError:
                        pass
                        # cv2.putText(img, text, (x,y), cv2.FONT_HERSHEY_COMPLEX, 1, (50,50,255), 1)

        # print(lang)
        # print(text)
        cv2.imshow('RESULT', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()



    def camcallback(self, instance):
        # change label text to "Hello + user name!"
        # self.greeting.text = "Hello " + self.user.text + "!"
        detect_language_api='7f2eddfd7b8fb4ad03628fbedbfb5aae'

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

        file=open("test.txt", "w", encoding="utf-8")
        rt = file.write(deftext)
        file.close()
        print(rt)

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
                    cv2.rectangle(img, (x,y), (w+x,h+y), (0,0,255), -1)
                    text = b[11]
                    try:
                        lang = single_detection(text, api_key=detect_language_api)
                        try:
                            translated_text = GoogleTranslator(source='auto', target='english').translate_file('test.txt')
                            cv2.putText(img, translated_text, (x,y), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 2)
                        except deep_translator.exceptions.InvalidSourceOrTargetLanguage:
                            cv2.putText(img, text, (x,y), cv2.FONT_HERSHEY_COMPLEX, 1, (50,50,255), 1)
                    except IndexError:
                        cv2.putText(img, text, (x,y), cv2.FONT_HERSHEY_COMPLEX, 1, (50,50,255), 1)

        # print(lang)
        # print(text)
        cv2.imshow('RESULT', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def pdfcallback(self, instance):
        # change label text to "Hello + user name!"
        # self.greeting.text = "Hello " + self.user.text + "!"
        file=open("sample2.pdf","rb")
        reader = PdfReader(file)
        # page = reader.pages[0]
        # print(page.extract_text())
        def readpdf():
            with open("sample2.pdf","rb") as f:
                reader=PdfReader(f)
                result=[]
                output=[]

                for i in range(0,len(reader.pages)): # prev read.getNumPages()
                    selected_page = reader.pages[i]
                    text = selected_page.extract_text()
                    result.append(text)
                    a=' '.join(result)
                    # print(len(a))
                    k=len(a)
                stj=0
                enj=4500
                for i in range(0,round(k/4500)+1):
                    file=open("translation.txt", "w", encoding="utf-8")
                    
                    rt = file.write(a[stj:enj])
                    # print(a)
                    file.close() # convert list to a single doc
                
                    translated_text = GoogleTranslator(source='auto', target='german').translate_file('translation.txt')
                    print(translated_text)

                    output.append(translated_text)
                    b=' '.join(output)
                    file=open("output.txt", "w", encoding="utf-8")
                    wr= file.write(b)
                    file.close()

                    stj=enj
                    enj=stj+4500

        readpdf()

    # def on_enter(instance, value):
    #     print('User pressed enter in', instance)


# run Say Hello App Calss
if __name__ == "__main__":
    SayHello().run()

