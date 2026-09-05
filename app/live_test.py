import asyncio
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client()

MODEL = "gemini-3.1-flash-live-preview"

# Connecting to the Live API (https://ai.google.dev/gemini-api/docs/live-api/get-started-sdk#connecting_to_the_live_api)
async def main():
    config = {
        "response_modalities": ["AUDIO"],
        "input_audio_transcription": {},
        "output_audio_transcription": {},
    }

    async with client.aio.live.connect(
        model=MODEL,
        config=config,
    ) as session:

     # Send content... its by me 

        print("SamvadAI Live session started.")
        
        # Sending audio as input
        # PCM audio (16-bit PCM audio, 16kHz, little-endian).

        # here sending text
        await session.send_realtime_input(
            text="Hello! Introduce yourself as SamvadAI in one sentence."
        )

        async for response in session.receive():

            if response.server_content:
                if response.server_content.output_transcription:
                    print(
                        "SamvadAI:",
                        response.server_content.output_transcription.text
                    )

                if response.server_content.turn_complete:
                    break


if __name__ == "__main__":
    asyncio.run(main())