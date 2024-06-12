async def stt(open_ai_client, file_name):
    audio_file = open(file_name, "rb")
    transcription = open_ai_client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file
    )
    text = transcription.text

    return text