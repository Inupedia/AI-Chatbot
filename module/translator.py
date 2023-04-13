import googletrans


class Translator():
    def translate_text(self, text: str) -> str:
        detect = self.detect_google(text)
        # translate to Japanese
        tts = self.translate_google(text, f"{detect}", "JA")
        # tts_en = self.translate_google(text, f"{detect}", "EN")
        # tts_cn = self.translate_google(text, f"{detect}", "ZH-CN")
        return tts

    def translate_google(self, text: str, source: str, target: str) -> str:
        try:
            translator = googletrans.Translator()
            result = translator.translate(text, src=source, dest=target)
            return result.text
        except:
            return f'Error translate {source} to {target}'

    def detect_google(self, text: str) -> str:
        try:
            translator = googletrans.Translator()
            result = translator.detect(text)
            return result.lang.upper()
        except:
            return f'Error detect {text}'
