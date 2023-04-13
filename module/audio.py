import pyaudio
import wave
import keyboard


class AudioRecorder():
    def __init__(self, config_data: dict):
        self.config_data = config_data

        # initialize pyaudio
        self.audio = pyaudio.PyAudio()

    def start(self) -> None:
        self.set_audio_input_device()
        print("Press and Hold Right Shift to record audio")

    # set the audio input device
    def set_audio_input_device(self) -> None:
        detection = input(
            "Do you need to adjust your microphone settings (y/n)? ")
        if detection == "y":
            self.list_recording_devices()
            audio_input_device = int(input("Enter the device index: "))
            # rewrite the config file
            self.config_data["device_index"] = audio_input_device

    # list all recording devices

    def list_recording_devices(self) -> None:
        for i in range(self.audio.get_device_count()):
            dev = self.audio.get_device_info_by_index(i)
            print((i, dev['name'], dev['maxInputChannels']))

    # record audio
    def record_audio(self) -> None:
        CHUNK = self.config_data["chunk"]
        FORMAT = pyaudio.paInt16
        CHANNELS = self.config_data["channels"]
        RATE = self.config_data["rate"]
        WAVE_OUTPUT_FILENAME = self.config_data["output_filename"]
        DEVICE_INDEX = self.config_data["device_index"]
        stream = self.audio.open(format=FORMAT,
                                 channels=CHANNELS,
                                 rate=RATE,
                                 input=True,
                                 frames_per_buffer=CHUNK,
                                 input_device_index=DEVICE_INDEX
                                 )
        frames = []
        print("Recording...")
        while keyboard.is_pressed('RIGHT_SHIFT'):
            data = stream.read(CHUNK)
            frames.append(data)
        print("Stop recording.")
        stream.stop_stream()
        stream.close()
        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(self.audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
