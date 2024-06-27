import uuid
import os
import asyncio

from aiogram import Bot, Dispatcher, html, F, types
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from openai import AsyncOpenAI
from aiogram.fsm.storage.redis import RedisStorage

from config import Settings
from db.DBManager import DBManager
from stt import stt
from tts import tts
from assistant import Assistant
from init_assistant import init_assistant
from get_emotion_in_image import get_emotion_in_image
from statistic.threadAmplitudeController import ThreadAmplitudeController

settings = Settings()
bot_token = settings.bot_token
open_ai_token = settings.open_ai_token
amplitude_api_key = settings.amplitude.amplitude_api_key
postgres = settings.postgres
redis = settings.redis

storage = RedisStorage.from_url(f"redis://{redis.redis_host}:{redis.redis_port}/{redis.redis_db}")

bot = Bot(token=bot_token)
dp = Dispatcher(storage=storage)
open_ai_client = AsyncOpenAI(api_key=open_ai_token)
thread_amplitude_controller = ThreadAmplitudeController(amplitude_api_key)

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

@dp.message(F.photo)
async def get_media(message: types.Message):
    file_id = message.photo[0].file_id
    file = await bot.get_file(file_id)

    url = "https://api.telegram.org/file/bot" + bot_token + "/" + file.file_path

    emotion = await get_emotion_in_image(open_ai_client, url)

    voice_message_path = await tts(open_ai_client, emotion)
    voice_message = types.FSInputFile(voice_message_path)
    await message.answer_voice(voice_message)
    os.remove(voice_message_path)
    thread_amplitude_controller.add_event("Определение эмоции по фото", str(message.from_user.id))

@dp.message(F.voice)
async def get_voice(message: Message, state: FSMContext) -> None:
    stream = await bot.download(message.voice)
    file_name = "./temp/temp" + str(uuid.uuid4()) + ".mp3"
    with open(file_name, "wb") as f:
        f.write(stream.getbuffer())
        f.close()
    text = await stt(open_ai_client, file_name)
    os.remove(file_name)

    sendMessage, thread_id = await assistant.send_question(text, state)
    answer_text = await assistant.get_answer(thread_id, sendMessage.id, message.from_user.id, thread_amplitude_controller)
    voice_message_path = await tts(open_ai_client, answer_text)
    voice_message = types.FSInputFile(voice_message_path)
    await message.answer_voice(voice_message)
    os.remove(voice_message_path)

async def main():
    await dp.start_polling(bot)

asyncio.run(main())