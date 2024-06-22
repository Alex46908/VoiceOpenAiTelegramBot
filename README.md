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
docker pull python:3.12-slim
docker build .
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
    instructions: str = "Узнай мои жизненные цености"
    error_message: str = "Я вас не понял. Давайте попробуем еще раз!"

# Text-To-Speech Settings
class ttsSettings(BaseSettings):
    model: str = "tts-1"
    voice: str = "alloy"
````

## So. Good luck!