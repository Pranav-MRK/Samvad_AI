import asyncio

from app.voice.audio import create_audio, open_microphone, open_speaker
from app.voice.session import VoiceSession


async def main():
    audio = create_audio()

    microphone = open_microphone(audio)
    speaker = open_speaker(audio)

    print("\n" + "=" * 60)
    print("🎙️ SamvadAI Voice Agent - DEBUG MODE")
    print("=" * 60)
    print("🎤 Speak into the microphone")
    print("🛑 Press Ctrl+C to stop")
    print("=" * 60 + "\n")

    input_chunks = 0
    output_chunks = 0
    input_text = ""
    output_text = ""

    try:
        async with VoiceSession() as voice:
            print("✅ Gemini Live connected")
            print(f"🔗 Session exists: {voice.session is not None}\n")

            async def send_audio():
                nonlocal input_chunks

                print("🎤 [SEND] Microphone loop started")

                try:
                    while True:
                        data = await asyncio.to_thread(
                            microphone.read,
                            1024,
                            exception_on_overflow=False,
                        )

                        input_chunks += 1

                        if input_chunks % 50 == 0:
                            print(
                                f"🎤 [SEND] Audio chunks sent: {input_chunks}",
                                flush=True,
                            )

                        await voice.send_audio(data)

                except asyncio.CancelledError:
                    print("🛑 [SEND] Microphone loop cancelled")
                    raise

                except Exception as e:
                    print(f"❌ [SEND] Error: {type(e).__name__}: {e}")
                    raise

            async def receive_audio():
                nonlocal output_chunks
                nonlocal input_text
                nonlocal output_text

                print("📥 [RECEIVE] Response loop started")

                try:
                    while True:
                        print("📡 [RECEIVE] Waiting for next response stream...")

                        async for response in voice.receive():

                            print(
                                f"\n📨 [RECEIVE] Response received: "
                                f"{type(response).__name__}",
                                flush=True,
                            )

                            server_content = getattr(
                                response,
                                "server_content",
                                None,
                            )

                            if server_content is not None:

                                input_transcription = getattr(
                                    server_content,
                                    "input_transcription",
                                    None,
                                )

                                if input_transcription is not None:
                                    text = getattr(
                                        input_transcription,
                                        "text",
                                        None,
                                    )

                                    if text:
                                        input_text += text

                                        print(
                                            f"👤 [INPUT] {text}",
                                            flush=True,
                                        )

                                output_transcription = getattr(
                                    server_content,
                                    "output_transcription",
                                    None,
                                )

                                if output_transcription is not None:
                                    text = getattr(
                                        output_transcription,
                                        "text",
                                        None,
                                    )

                                    if text:
                                        output_text += text

                                        print(
                                            f"🤖 [OUTPUT] {text}",
                                            flush=True,
                                        )

                                turn_complete = getattr(
                                    server_content,
                                    "turn_complete",
                                    False,
                                )

                                if turn_complete:
                                    print("\n✅ [TURN COMPLETE]")

                                    if input_text:
                                        print(f"👤 Full input: {input_text}")

                                    if output_text:
                                        print(f"🤖 Full output: {output_text}")

                                    print("-" * 60)

                                    input_text = ""
                                    output_text = ""

                            data = getattr(response, "data", None)

                            if data:
                                output_chunks += 1
                                speaker.write(data)

                        print(
                            "⚠️ [RECEIVE] Response stream ended. "
                            "Re-entering receive stream..."
                        )

                        await asyncio.sleep(0.1)

                except asyncio.CancelledError:
                    print("🛑 [RECEIVE] Response loop cancelled")
                    raise

                except Exception as e:
                    print(
                        f"❌ [RECEIVE] Error: "
                        f"{type(e).__name__}: {e}"
                    )
                    raise

                finally:
                    print("📥 [RECEIVE] Response loop ended")
            send_task = asyncio.create_task(send_audio())
            receive_task = asyncio.create_task(receive_audio())

            print("🚀 Both voice tasks started\n")

            try:
                await asyncio.gather(
                    send_task,
                    receive_task,
                )

            except Exception as e:
                print(
                    f"\n❌ Voice loop failed: "
                    f"{type(e).__name__}: {e}"
                )

                print(
                    f"📊 Input chunks: {input_chunks}"
                )
                print(
                    f"📊 Output chunks: {output_chunks}"
                )

                send_task.cancel()
                receive_task.cancel()

                await asyncio.gather(
                    send_task,
                    receive_task,
                    return_exceptions=True,
                )

                raise

    except KeyboardInterrupt:
        print("\n🛑 Ctrl+C received")

    except Exception as e:
        print(
            f"\n❌ Main voice session error: "
            f"{type(e).__name__}: {e}"
        )

    finally:
        print("\n🧹 Cleaning up audio...")

        microphone.stop_stream()
        microphone.close()

        speaker.stop_stream()
        speaker.close()

        audio.terminate()

        print("✅ SamvadAI stopped cleanly")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Process interrupted")