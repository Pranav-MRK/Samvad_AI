import asyncio
import os
import pyaudio

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODEL = "gemini-3.1-flash-live-preview"

FORMAT = pyaudio.paInt16
CHANNELS = 1
INPUT_RATE = 16000
OUTPUT_RATE = 24000
CHUNK = 1024

async def main():
    audio = pyaudio.PyAudio()

    microphone = audio.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=INPUT_RATE,
        input=True,
        frames_per_buffer=CHUNK,
    )

    speaker = audio.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=OUTPUT_RATE,
        output=True,
        frames_per_buffer=CHUNK,
    )

    config = {
        "response_modalities": ["AUDIO"],
        "input_audio_transcription": {},
        "output_audio_transcription": {},
    }

    print("Connecting to SamvadAI...")


    async with client.aio.live.connect(model=MODEL, config=config) as session:
        print("SamvadAI is listening. Speak now.")
        print("Press Ctrl+C to stop.")
        async def send_audio():
            while True:
                data = await asyncio.to_thread(
                    microphone.read,
                    CHUNK,
                    exception_on_overflow=False,
                )
                await session.send_realtime_input(
                    audio={
                        "data": data,
                        "mime_type": "audio/pcm;rate=16000",
                    }
                )

        async def receive_audio():
            async for response in session.receive():
                if response.data:
                    await asyncio.to_thread(
                        speaker.write,
                        response.data,
                    )
                if response.server_content:
                    if response.server_content.input_transcription:
                        text = response.server_content.input_transcription.text
                        if text:
                            print("You:", text)
                    if response.server_content.output_transcription:
                        text = response.server_content.output_transcription.text
                        if text:
                            print("SamvadAI:", text)

        try:
            await asyncio.gather(
                send_audio(),
                receive_audio(),
            )

        finally:
            microphone.stop_stream()
            microphone.close()

            speaker.stop_stream()
            speaker.close()

            audio.terminate()                


if __name__ == "__main__":
    asyncio.run(main())



    