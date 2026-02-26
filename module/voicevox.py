from urllib.parse import urlencode
import requests


class Voice():
    def __init__(self, config_data: dict):
        self.voice_api_endpoint = config_data["endpoint"]
        self.filename = config_data["output_filename"]
        self.character_id = config_data["speaker_id"]

    def voicevox_tts(self, text: str):
        try:
            params_encoded = urlencode(
                {'text': text, 'speaker': self.character_id})
            r = requests.post(
                f'{self.voice_api_endpoint}/audio_query?{params_encoded}',
                timeout=10)

            if r.status_code == 404:
                print('Unable to reach Voicevox, ensure that it is running, or the endpoint is set correctly')
                return
            r.raise_for_status()

            params_encoded = urlencode({'speaker': self.character_id})
            result = requests.post(
                f'{self.voice_api_endpoint}/synthesis?{params_encoded}',
                json=r.json(),
                timeout=30)
            result.raise_for_status()

            with open(self.filename, 'wb') as f:
                f.write(result.content)
        except requests.ConnectionError:
            print(f'Cannot connect to Voicevox at {self.voice_api_endpoint}. Is the engine running?')
        except requests.Timeout:
            print('Voicevox request timed out')
        except Exception as e:
            print(f'Voicevox TTS error: {e}')
