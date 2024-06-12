import uuid
from config import Settings

settings = Settings()

def tts(open_ai_client, text):
    speech_file_path = "./temp/temp" + str(uuid.uuid4()) + ".mp3"
    response = open_ai_client.audio.speech.create(
        model=settings.tts.model,
        voice=settings.tts.voice,
        input=text
    )
    response.stream_to_file(speech_file_path)

    return speech_file_path