import whisper

class SpeechToText:
    def __init__(self):
        self.model = whisper.load_model("base")

    def transcribe(self, audio_file):
        result = self.model.transcribe(audio_file, fp16=False)
        return result["text"]