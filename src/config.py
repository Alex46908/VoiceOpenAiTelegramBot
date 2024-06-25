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
    instructions: str = "Узнай мои жизненные цености"
    assistant_id: str = Field("", env="ASSISTANT_ID")
    error_message: str = "Я вас не понял. Давайте попробуем еще раз!"

# Amplitude Settings
class anplitudeSettings(BaseSettings):
    amplitude_api_key: str = Field("", env="ASSISTANT_API_KEY")

# Text-To-Speech Settings
class ttsSettings(BaseSettings):
    model: str = "tts-1"
    voice: str = "alloy"


# Postgres Settings
class postgresSettings(BaseSettings):
    postgres_user: str = Field("user", env="POSTGRES_USER")
    postgres_password: str = Field("password", env="POSTGRES_PASSWORD")
    postgres_host: str = Field("host", env="POSTGRES_HOST")
    postgres_port: str = Field("port", env="POSTGRES_PORT")
    postgres_db: str = Field("db", env="POSTGRES_DB")

class Settings(BaseSettings):
    open_ai_token: str = Field("", env="OPEN_AI_TOKEN")
    bot_token: str = Field("", env="BOT_TOKEN")
    tts: BaseSettings  = ttsSettings()
    assistant: BaseSettings = assistantSettings()
    stt: BaseSettings = sttSettings()
    postgres: BaseSettings = postgresSettings()
    amplitude: BaseSettings = anplitudeSettings()