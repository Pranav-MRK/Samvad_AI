import asyncio

from app.voice.audio import create_audio, open_microphone, open_speaker
from app.voice.session import VoiceSession


async def microphone_loop(voice, microphone):
    try:
        while True:
            data = await asyncio.to_thread(
                microphone.read,
                1024,
                exception_on_overflow=False,
            )

            await voice.send_audio(data)

    except asyncio.CancelledError:
        pass


async def speaker_loop(voice, speaker):
    try:
        async for response in voice.receive():
            if response.data:
                await asyncio.to_thread(speaker.write, response.data)

            if response.server_content:
                if response.server_content.input_transcription:
                    transcript = response.server_content.input_transcription.text
                    if transcript:
                        print(f"You: {transcript}")

                if response.server_content.output_transcription:
                    transcript = response.server_content.output_transcription.text
                    if transcript:
                        print(f"SamvadAI: {transcript}")

    except asyncio.CancelledError:
        pass


async def main():
    audio = create_audio()

    microphone = open_microphone(audio)
    speaker = open_speaker(audio)

    try:
        async with VoiceSession() as voice:
            print("🎙️ SamvadAI is listening. Speak now.")
            print("Press Ctrl+C to stop.")

            mic_task = asyncio.create_task(
                microphone_loop(voice, microphone)
            )

            speaker_task = asyncio.create_task(
                speaker_loop(voice, speaker)
            )

            try:
                await asyncio.gather(mic_task, speaker_task)

            except asyncio.CancelledError:
                pass

    finally:
        microphone.stop_stream()
        microphone.close()

        speaker.stop_stream()
        speaker.close()

        audio.terminate()

        print("\n SamvadAI stopped.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n Shutting down...")