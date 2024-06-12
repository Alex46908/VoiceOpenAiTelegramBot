import uuid

def tts(open_ai_client, text):
    speech_file_path = "./temp/temp" + str(uuid.uuid4()) + ".mp3"
    response = open_ai_client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text
    )
    response.stream_to_file(speech_file_path)

    return speech_file_path