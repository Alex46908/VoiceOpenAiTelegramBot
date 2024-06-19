import uuid
import os
import asyncio

from aiogram import Bot, Dispatcher, html, F, types
from aiogram.types import Message
from openai import AsyncOpenAI

from config import Settings
from stt import stt
from tts import tts
import assistant as Assistant

settings = Settings()
bot_token = settings.bot_token
open_ai_token = settings.open_ai_token

bot = Bot(token=bot_token)
dp = Dispatcher()
open_ai_client = AsyncOpenAI(api_key=open_ai_token)

async def init_assistant():
    assistant = await Assistant.init(open_ai_client)
    Settings.assistant_id = assistant.id

asyncio.run(init_assistant())

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

    sendMessage, thread = await Assistant.send_question(open_ai_client, text)
    answer_text = await Assistant.get_answer(open_ai_client, Settings.assistant_id, thread.id, sendMessage.id)

    voice_message_path = await tts(open_ai_client, answer_text)
    voice_message = types.FSInputFile(voice_message_path)
    await message.answer_voice(voice_message)
    os.remove(voice_message_path)

async def main():
    await dp.start_polling(bot)

asyncio.run(main())