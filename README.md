# VoiceOpenAiTelegramBot

***

## Installation
### 1. Add .env
#### Path: src/.env
#### .env Example:
````
OPEN_AI_TOKEN=*open_ai_token
BOT_TOKEN=*bot_token
````
### 2. Install requirements
````
//for linux and mac
pip3 install -r requirements.txt

//for windows
pip install -r requirements.txt
````

***

## Start
````
//for linux and mac
python3 src/main.py

//for windows
python src/main.py
````

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
    instructions: str = "Speak with user"

# Text-To-Speech Settings
class ttsSettings(BaseSettings):
    model: str = "tts-1"
    voice: str = "alloy"
````

## So. Good luck!