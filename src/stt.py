from config import Settings

settings = Settings()

async def stt(open_ai_client, file_name):
    audio_file = open(file_name, "rb")
    transcription = await open_ai_client.audio.transcriptions.create(
        model=settings.stt.model,
        file=audio_file
    )
    text = transcription.text
    audio_file.close()

    return text