import json
import os
import queue
import threading
from typing import List, Union
from pydub import AudioSegment
from pydub.playback import play
from module.translator import Translator
from module.voicevox import Voice
from module.chatgpt import ChatGPT
from module.gemini import Gemini
from module.bilibili import BilibiliLive

ChatSession = Union[ChatGPT, Gemini]


def create_session(config_data: dict, username: str) -> ChatSession:
    provider = config_data.get("provider", "openai")
    if provider == "gemini":
        return Gemini(config_data, username=username)
    return ChatGPT(config_data, username=username)


class AIVtuber():

    sessions: List[ChatSession] = []
    audio_recorder = None

    def __init__(self):
        config_file_path = os.path.join(
            os.path.dirname(__file__), "config.json")

        with open(config_file_path, 'r', encoding='utf-8') as f:
            self.config_data = json.load(f)

        provider = self.config_data.get("provider", "openai")
        print(f"Using AI provider: {provider}")

        self.session = create_session(
            self.config_data, username=self.config_data["username"])

        AIVtuber.sessions.append(self.session)

        self.translator = Translator()

        self.voice = Voice(self.config_data["voicevox"])

        self.message_queue = queue.Queue(self.config_data["queue_size"])
        self.message_thread = threading.Thread(target=self.get_result_in_queue)
        self.message_thread.daemon = True
        self.message_thread.start()

    def get_config_data(self) -> dict:
        return self.config_data

    def chat(self):
        if self.config_data['chat_mode'] == 'text':
            self.text_chat(self.config_data['username'])
        elif self.config_data['chat_mode'] == 'voice':
            import keyboard
            from module.audio import AudioRecorder
            from module.whisper import SpeechToText
            self.whisper_stt = SpeechToText()
            AIVtuber.audio_recorder = AudioRecorder(self.config_data['audio'])
            self.voice_chat(self.config_data['username'])
        elif self.config_data['chat_mode'] == 'live':
            self.live_chat()

    def text_chat(self, username: str):
        print("Type 'exit' to exit the chat")
        prompt = input("User: ")
        while prompt != 'exit':
            self.message_queue.put((username, prompt))
            prompt = input("User: ")

    def voice_chat(self, username: str):
        import keyboard
        AIVtuber.audio_recorder.start()
        try:
            while True:
                if keyboard.is_pressed('RIGHT_SHIFT'):
                    AIVtuber.audio_recorder.record_audio()
                    self.process_recording(username)
                    self.get_result(username)
        except KeyboardInterrupt:
            print("Stopped")

    def live_chat(self):
        b_live = BilibiliLive(self.config_data["room_id"], self.message_queue)
        b_live.start()

    def get_result(self, username: str):
        current_session = self.get_session(username)
        assistant_message = current_session.get_response()
        self.text_to_speech(assistant_message)
        print(f"AI Vtuber: {assistant_message}")
        self.play_audio(self.config_data["voicevox"]["output_filename"])

    def get_result_in_queue(self):
        while True:
            if self.message_queue.full():
                for i in range(self.config_data["queue_size"] // 2):
                    self.message_queue.get()
            try:
                username, message = self.message_queue.get()
                current_session = self.get_session(username)
                current_session.add_current_message(message)
                assistant_message = current_session.get_response()
                self.text_to_speech(assistant_message)
                print(f'User: {message}')
                print(f"AI Vtuber: {assistant_message}")
                self.play_audio(
                    self.config_data["voicevox"]["output_filename"])
            except queue.Empty:
                pass

    def process_recording(self, username: str):
        content: str = self.speech_to_text(
            self.config_data["audio"]["output_filename"])
        current_session = self.get_session(username)
        current_session.add_current_message(content)

    def speech_to_text(self, audio_file: str) -> str:
        try:
            text = self.whisper_stt.transcribe(audio_file)
            return text
        except Exception as e:
            return f"Error: {e}"

    def text_to_speech(self, message: str):
        message_jp = self.translator.translate_text(message)
        self.voice.voicevox_tts(message_jp)

    def play_audio(self, audio_file: str):
        try:
            sound = AudioSegment.from_file(audio_file)
            play(sound)
        except Exception as e:
            print(f"Error playing audio: {e}")

    def get_session(self, username: str) -> ChatSession:
        for session in AIVtuber.sessions:
            if session.username == username:
                return session
        new_session = create_session(self.config_data, username)
        AIVtuber.sessions.append(new_session)
        return new_session
