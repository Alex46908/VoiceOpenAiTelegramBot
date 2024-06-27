# VoiceOpenAiTelegramBot

***

## Installation
### 1. Add .env
#### Path: src/.env
#### You can watch example in ./src/.env.example:

### 2. Install requirements
````
//for linux and mac
pip3 install -r requirements.txt

//for windows
pip install -r requirements.txt
````

***

## Before first start, migrate db:
````
    alembic upgrade head
````

***

## Start
````
//for linux and mac
python3 src/main.py

//for windows
python src/main.py
````

## If you start project first time, you will see:
````
Assistant ID not set
Assistant created successfully!
Please, add to .env:
ASSISTANT_ID=...
````
### Please, follow the instructions


***

## Build
````
Add postgres user and password in docker-compose.yaml (line 31, 32)
docker-compose build
````

****

## Configuration and Settings
### You can change settings in src/config.py
````
# Speech-To-Text Settings
class sttSettings(BaseSettings):
    model: str = "whisper-1"

# Assistant Settings
class assistantSettings(BaseSettings):
    model: str = "gpt-4o"
    vector_storage_id: str = Field("", env="VECTOR_STORAGE_ID")
    instructions: str = "Узнай мои жизненные цености."
    assistant_id: str = Field("", env="ASSISTANT_ID")
    error_message: str = self"Я вас не понял. Давайте попробуем еще раз!"

# Redis Settings
class redisSettings(BaseSettings):
    redis_host: str = Field("", env="REDIS_HOST")
    redis_port: int = Field("", env="REDIS_PORT")
    redis_db: int = Field("", env="REDIS_DB")

# Amplitude Settings
class anplitudeSettings(BaseSettings):
    amplitude_api_key: str = Field("", env="ASSISTANT_API_KEY")

# Text-To-Speech Settings
class ttsSettings(BaseSettings):
    model: str = "tts-1"
    voice: str = "alloy"
````

## So. Good luck!