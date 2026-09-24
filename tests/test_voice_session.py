import asyncio

from app.voice.session import VoiceSession


async def main():
    async with VoiceSession() as voice:
        print("✅ VoiceSession connected")
        print("Session:", voice.session is not None)

    print("✅ VoiceSession closed")


if __name__ == "__main__":
    asyncio.run(main())