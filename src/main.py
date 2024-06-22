import uuid
import os
import asyncio

from aiogram import Bot, Dispatcher, html, F, types
from aiogram.types import Message
from openai import AsyncOpenAI

from config import Settings
from db.DBManager import DBManager
from stt import stt
from tts import tts
from assistant import Assistant
from init_assistant import init_assistant

settings = Settings()
bot_token = settings.bot_token
open_ai_token = settings.open_ai_token
postgres = settings.postgres

bot = Bot(token=bot_token)
dp = Dispatcher()
open_ai_client = AsyncOpenAI(api_key=open_ai_token)

async def init_new_assistant():
    print("Assistant ID not set")
    await init_assistant(open_ai_client)
    exit(200)

if settings.assistant.assistant_id == "":
    asyncio.run(init_new_assistant())

db_manager = DBManager(
    user=postgres.postgres_user,
    password=postgres.postgres_password,
    host=postgres.postgres_host,
    port=postgres.postgres_port,
    db=postgres.postgres_db
)
asyncio.run(db_manager.connect())

assistant = Assistant(open_ai_client, db_manager)

os.makedirs('./temp', exist_ok=True)

@dp.message(F.voice)
async def get_voice(message: Message) -> None:
    stream = await bot.download(message.voice)
    file_name = "./temp/temp" + str(uuid.uuid4()) + ".mp3"
    with open(file_name, "wb") as f:
        f.write(stream.getbuffer())
        f.close()
    text = await stt(open_ai_client, file_name)
    os.remove(file_name)

    sendMessage, thread = await assistant.send_question(text)
    answer_text = await assistant.get_answer(thread.id, sendMessage.id, message.from_user.id)

    voice_message_path = await tts(open_ai_client, answer_text)
    voice_message = types.FSInputFile(voice_message_path)
    await message.answer_voice(voice_message)
    os.remove(voice_message_path)

async def main():
    await dp.start_polling(bot)

asyncio.run(main())