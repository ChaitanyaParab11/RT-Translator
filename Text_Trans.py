from translate import Translator


def texttranslate(ptext):
    lang="German"
    translator= Translator(to_lang=lang)
    translation = translator.translate(ptext.capitalize())
    print(translation)
    return translation