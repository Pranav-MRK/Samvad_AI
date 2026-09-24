from google import genai


from app.core.config import GEMINI_API_KEY, GEMINI_LIVE_MODEL


class VoiceSession:
    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self._cm = None
        self.session = None

    async def connect(self):
        self._cm = self.client.aio.live.connect(
            model=GEMINI_LIVE_MODEL,
            # pyrefly: ignore [bad-argument-type]
            config={
                "response_modalities": ["AUDIO"],
                "input_audio_transcription": {},
                "output_audio_transcription": {},
            }, # type: ignore
        )
        self.session = await self._cm.__aenter__()
        return self.session

    async def send_audio(self, data: bytes):
        if not self.session:
            raise RuntimeError("VoiceSession is not connected. Call connect() first.")
        await self.session.send_realtime_input(
            audio={
                "data": data,
                "mime_type": "audio/pcm;rate=16000",
            }
        )

    async def receive(self):
        if not self.session:
            raise RuntimeError("VoiceSession is not connected. Call connect() first.")
        async for response in self.session.receive():
            yield response

    async def close(self):
        if self._cm:
            await self._cm.__aexit__(None, None, None)
            self.session = None
            self._cm = None

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
