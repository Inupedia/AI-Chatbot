from urllib.parse import urlencode
import requests


class Voice():
    def __init__(self, config_data: dict):
        # voicevox docs:
        #
        # Args:
        #     voice_api_endpoint (str): voice api endpoint
        #     character_id (int): character index
        #
        self.voice_api_endpoint = config_data["endpoint"]
        self.filename = config_data["output_filename"]
        self.character_id = config_data["speaker_id"]

    def voicevox_tts(self, text: str) -> None:

        # initial request with text
        params_encoded = urlencode(
            {'text': text, 'speaker': self.character_id})
        r = requests.post(
            f'{self.voice_api_endpoint}/audio_query?{params_encoded}')

        if r.status_code == 404:
            print('Unable to reach Voicevox, ensure that it is running, or the VOICEVOX_BASE_URL variable is set correctly')
            return

        # request to get audio
        params_encoded = urlencode({'speaker': self.character_id})
        result = requests.post(
            f'{self.voice_api_endpoint}/synthesis?{params_encoded}', json=r.json())

        # save audio
        with open(self.filename, 'wb') as f:
            f.write(result.content)
