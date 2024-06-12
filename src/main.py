import uuid
import os

from telegram import Update
from telegram.ext import ApplicationBuilder, CallbackContext, MessageHandler, filters
from openai import OpenAI

from config import Settings
from stt import stt
from tts import tts
import assistant as Assistant

settings = Settings()
bot_token = settings.bot_token
open_ai_token = settings.open_ai_token

app = ApplicationBuilder().token(bot_token).build()
open_ai_client = OpenAI(api_key=open_ai_token)
assistant, thread = Assistant.init(open_ai_client)

os.makedirs('./temp', exist_ok=True)

async def get_voice(update: Update, context: CallbackContext) -> None:
    new_file = await context.bot.get_file(update.message.voice.file_id)
    file_name = "./temp/temp" + str(uuid.uuid4()) +".mp3"
    await new_file.download_to_drive(file_name)
    text = await stt(open_ai_client, file_name)
    os.remove(file_name)

    message = Assistant.send_question(open_ai_client, thread.id, text)
    answer_text = Assistant.get_answer(open_ai_client, assistant.id, thread.id, message.id)

    voice_message_path = tts(open_ai_client, answer_text)
    await update.message.reply_voice(voice_message_path)
    os.remove(voice_message_path)

app.add_handler(MessageHandler(filters.VOICE, get_voice))

app.run_polling()
