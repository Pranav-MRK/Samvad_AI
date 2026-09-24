import pyaudio


FORMAT = pyaudio.paInt16
CHANNELS = 1

INPUT_RATE = 16000
OUTPUT_RATE = 24000

CHUNK = 1024


def create_audio():
    return pyaudio.PyAudio()


def open_microphone(audio):
    return audio.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=INPUT_RATE,
        input=True,
        frames_per_buffer=CHUNK,
    )


def open_speaker(audio):
    return audio.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=OUTPUT_RATE,
        output=True,
        frames_per_buffer=CHUNK,
    )