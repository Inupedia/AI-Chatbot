import keyboard
import json
import os
import openai
from pydub import AudioSegment
from pydub.playback import play
from module.translator import Translator
from module.audio import AudioRecorder
from module.voicevox import Voice


class AIVtuber():

    # list of all conversation between the user and the AI Vtuber
    conversation: list = []

    audio_recorder: AudioRecorder = None

    def __init__(self):
        '''
        Initialize the AI_Vtuber parameters.
        Args:
            audio_input_device (int, optional): The index of the audio input device. Defaults to 0.
        '''
        config_file_path = os.path.join(
            os.path.dirname(__file__), "config.json")

        with open(config_file_path, 'r') as f:
            self.config_data = json.load(f)

        # set up openai api key & personality
        openai.api_key = self.config_data["openai"]["api_key"]

        # initialize the personality of the AI vtuber
        AIVtuber.conversation.append(
            {'role': 'system', 'content': self.config_data["chatgpt"]["role"]})

        # initialize the current message
        self.current_message = {'role': 'user', 'content': ''}

        # initialize the translator
        self.translator = Translator()

        # initialize the voice synthesizer
        self.voice = Voice(self.config_data["voicevox"])

    def get_config_data(self) -> dict:
        return self.config_data

    def chat(self) -> None:
        if (self.config_data['chat_mode'] == 'text'):
            self.text_chat()
        elif (self.config_data['chat_mode'] == 'voice'):
            AIVtuber.audio_recorder = AudioRecorder(self.config_data['audio'])
            self.voice_chat()

    def text_chat(self) -> None:
        print("Type 'exit' to exit the chat")
        prompt = input("User: ")
        while prompt != 'exit':
            self.current_message['content'] = prompt
            AIVtuber.conversation.append(self.current_message)
            self.get_result()
            prompt = input("User: ")

    def voice_chat(self) -> None:
        AIVtuber.audio_recorder.start()
        try:
            while True:
                if keyboard.is_pressed('RIGHT_SHIFT'):
                    AIVtuber.audio_recorder.record_audio()
                    self.process_recording()
                    self.get_result()
        except KeyboardInterrupt:
            print("Stopped")

    def get_result(self):
        self.get_response_from_chatgpt()
        self.text_to_speech()
        # print(AIVtuber.conversation)
        print(f"AI Vtuber: {AIVtuber.conversation[-1]['content']}")
        self.play_audio(self.config_data["voicevox"]["output_filename"])

    def process_recording(self) -> None:
        self.current_message['content'] = self.speech_to_text(
            self.config_data["audio"]["output_filename"])
        AIVtuber.conversation.append(
            {'role': 'user', 'content': self.current_message['content']})

    # using openai whisper api to convert the speech to text

    def speech_to_text(self, audio_file: str) -> str:
        try:
            audio_file = open(audio_file, "rb")
            transcript = openai.Audio.transcribe("whisper-1", audio_file)
            return transcript.text
        except Exception as e:
            return f"Error: {e}"

    # text to speech (voicevox engine as an example)
    def text_to_speech(self) -> None:
        message_jp = self.translator.translate_text(
            AIVtuber.conversation[-1]['content'])
        self.voice.voicevox_tts(message_jp)

    # play the audio file
    def play_audio(self, audio_file: str) -> None:
        sound = AudioSegment.from_file(audio_file)
        play(sound)

    def get_response_from_chatgpt(self) -> str:
        try:
            resp = openai.ChatCompletion.create(
                model=self.config_data['chatgpt']['model'],
                messages=AIVtuber.conversation,
                max_tokens=self.config_data['chatgpt']['max_tokens'],
                temperature=self.config_data['chatgpt']['temperature'],
                top_p=self.config_data['chatgpt']['top_p'],
                frequency_penalty=self.config_data['chatgpt']['frequency_penalty'],
                presence_penalty=self.config_data['chatgpt']['presence_penalty']
            )
            content = resp['choices'][0]['message']['content']
            AIVtuber.conversation.append(
                {'role': 'assistant', 'content': content})
            return content
        except openai.OpenAIError as e:
            return f"Error: {e}"
