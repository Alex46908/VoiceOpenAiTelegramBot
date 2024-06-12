from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()

# Speech-To-Text Settings
class sttSettings(BaseSettings):
    model: str = "whisper-1"

# Assistant Settings
class assistantSettings(BaseSettings):
    model: str = "gpt-4o"
    instructions: str = "Speak with user"

# Text-To-Speech Settings
class ttsSettings(BaseSettings):
    model: str = "tts-1"
    voice: str = "alloy"

class Settings(BaseSettings):
    open_ai_token: str = Field("", env="OPEN_AI_TOKEN")
    bot_token: str = Field("", env="BOT_TOKEN")
    tts: BaseSettings  = ttsSettings()
    assistant: BaseSettings = assistantSettings()
    stt: BaseSettings = sttSettings()