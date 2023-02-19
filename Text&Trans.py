from translate import Translator

ptext=input("Enter your text: ")
lang="German"
translator= Translator(to_lang=lang)
translation = translator.translate(ptext.capitalize())
print(translation)