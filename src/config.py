from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()
class Settings(BaseSettings):
    open_ai_token: str = Field("", env="OPEN_AI_TOKEN")
    bot_token: str = Field("", env="BOT_TOKEN")