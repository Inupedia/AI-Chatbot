from deep_translator import GoogleTranslator


class Translator():
    def translate_text(self, text: str) -> str:
        tts = self.translate_google(text, "auto", "ja")
        return tts

    def translate_google(self, text: str, source: str, target: str) -> str:
        try:
            translator = GoogleTranslator(source=source, target=target)
            result = translator.translate(text)
            return result
        except Exception as e:
            return f'Error translating to {target}: {e}'
