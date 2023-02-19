from PyPDF2 import PdfReader,PdfWriter,PdfFileReader
from deep_translator import GoogleTranslator
from translate import Translator


def pdftranslate():
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