from langdetect import detect
import langcodes


def detectLanguage(text = str):
    try:
        langcode = detect(text) #returns 2 character language code, one of 55 languages "out of the box" according to pypi
        return langcodes.get(langcode).language_name() #returns english name of the language associated with the above language code
    except:
        return "Unknown Language"