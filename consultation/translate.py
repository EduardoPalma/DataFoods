from deep_translator import GoogleTranslator, ChatGptTranslator, MyMemoryTranslator
from libretranslatepy import LibreTranslateAPI


class Translate:

    @staticmethod
    def translate_google(text_, language, from_language="auto"):
        return GoogleTranslator(source=from_language, target=language).translate_batch(text_)

    @staticmethod
    def translate_google_single(text_, language, from_language="auto"):
        return GoogleTranslator(source=from_language, target=language).translate(text_)

    @staticmethod
    def translate_gpt(text_, language, from_language="spanish"):
        return ChatGptTranslator(api_key="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", source=from_language,
                                 target=language).translate(text=text_)

    @staticmethod
    def translate_memory(text_, language, from_language='es-419'):
        return MyMemoryTranslator(source=from_language, target=language).translate(text_)

    @staticmethod
    def translate_libre_translate(text_, language, from_languaje='es'):
        lt = LibreTranslateAPI("https://translate.argosopentech.com/")
        return lt.translate(text_, from_languaje, language)
