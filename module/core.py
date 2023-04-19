import keyboard
import json
import os
import openai
import queue
import threading
from typing import List
from pydub import AudioSegment
from pydub.playback import play
from module.translator import Translator
from module.audio import AudioRecorder
from module.voicevox import Voice
from module.chatgpt import ChatGPT
from module.bilibili import BilibiliLive


class AIVtuber():

    # list of all conversation between the user and the AI Vtuber
    chatgpt_sessions: List[ChatGPT] = []

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

        # set up openai api key
        openai.api_key = self.config_data["openai"]["api_key"]

        # initialize the chatgpt session
        self.chatgpt_session = ChatGPT(
            self.config_data, username=self.config_data["username"])

        # add the chatgpt session to the list
        AIVtuber.chatgpt_sessions.append(self.chatgpt_session)

        # initialize the translator
        self.translator = Translator()

        # initialize the voice synthesizer
        self.voice = Voice(self.config_data["voicevox"])

        # message queue
        self.message_queue = queue.Queue(self.config_data["queue_size"])
        self.message_thread = threading.Thread(target=self.get_result_in_queue)
        self.message_thread.daemon = True
        self.message_thread.start()

    def get_config_data(self) -> dict:
        return self.config_data

    def chat(self):
        if (self.config_data['chat_mode'] == 'text'):
            self.text_chat(self.config_data['username'])
        if (self.config_data['chat_mode'] == 'voice'):
            AIVtuber.audio_recorder = AudioRecorder(self.config_data['audio'])
            self.voice_chat(self.config_data['username'])
        if (self.config_data['chat_mode'] == 'live'):
            self.live_chat()

    def text_chat(self, username: str):
        print("Type 'exit' to exit the chat")
        prompt = input("User: ")
        while prompt != 'exit':
            # current_user_session = self.get_session(username)
            # current_user_session.add_current_message(prompt)
            # push current username with its message to the queue
            self.message_queue.put((username, prompt))
            # self.get_result(username)
            prompt = input("User: ")

    def voice_chat(self, username: str):
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
        # username, message = b_live.on_danmaku()
        # self.message_queue.put((username, message))
        # print(f"{username}: {message}")

    def get_result(self, username: str):
        # self.get_response_from_chatgpt()
        current_user_session = self.get_session(username)
        assistant_message = current_user_session.get_response_from_chatgpt()
        self.text_to_speech(assistant_message)
        # print(AIVtuber.conversation)
        print(f"AI Vtuber: {assistant_message}")
        self.play_audio(self.config_data["voicevox"]["output_filename"])

    def get_result_in_queue(self):
        while True:
            # if the queue is full, remove half of the oldest messages
            if self.message_queue.full():
                for i in range(self.config_data["queue_size"] // 2):
                    self.message_queue.get()
            try:
                username, message = self.message_queue.get()
                current_user_session = self.get_session(username)
                current_user_session.add_current_message(message)
                assistant_message = current_user_session.get_response_from_chatgpt()
                self.text_to_speech(assistant_message)
                # print(AIVtuber.conversation)
                print(f'User: {message}')
                print(f"AI Vtuber: {assistant_message}")
                self.play_audio(
                    self.config_data["voicevox"]["output_filename"])
            except queue.Empty:
                pass

    def process_recording(self, username: str):
        content: str = self.speech_to_text(
            self.config_data["audio"]["output_filename"])
        current_user_session = self.get_session(username)
        current_user_session.add_current_message(content)

    # using openai whisper api to convert the speech to text

    def speech_to_text(self, audio_file: str) -> str:
        try:
            audio_file = open(audio_file, "rb")
            transcript = openai.Audio.transcribe("whisper-1", audio_file)
            return transcript.text
        except Exception as e:
            return f"Error: {e}"

    # text to speech (voicevox engine as an example)
    def text_to_speech(self, message: str):
        message_jp = self.translator.translate_text(message)
        self.voice.voicevox_tts(message_jp)

    # play the audio file
    def play_audio(self, audio_file: str):
        sound = AudioSegment.from_file(audio_file)
        play(sound)

    # get the session base on the username, if the session does not exist, create a new one
    def get_session(self, username: str) -> ChatGPT:
        for session in AIVtuber.chatgpt_sessions:
            if session.username == username:
                return session
            else:
                AIVtuber.chatgpt_sessions.append(
                    ChatGPT(self.config_data, username))
                return AIVtuber.chatgpt_sessions[-1]
