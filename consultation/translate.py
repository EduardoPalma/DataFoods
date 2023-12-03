
from deep_translator import GoogleTranslator, MyMemoryTranslator
from googletrans import Translator


class Translate:

    @staticmethod
    def translate_google(text_, language, from_language="auto"):
        return GoogleTranslator(source=from_language, target=language).translate_batch(text_)

    @staticmethod
    def translate_google_single(text_, language, from_language="auto"):
        return GoogleTranslator(source=from_language, target=language).translate(text_)

    @staticmethod
    def translate_memory(text_, language, from_language='es-419'):
        return MyMemoryTranslator(source=from_language, target=language).translate_batch(text_)


    @staticmethod
    def translate_batch(texts, source_language='en', target_language='es'):
        translator = Translator()
        trans = [translator.translate(text, src=source_language, dest=target_language).text for text in texts]
        return trans

