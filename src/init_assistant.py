from config import Settings

settings = Settings()

async def init_assistant(open_ai_client):
    assistant = await open_ai_client.beta.assistants.create(
        model=settings.assistant.model,
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "save_value",
                    "description": "Save user life value. If return False don't say about it",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "value": {
                                "type": "string",
                                "description": "User life value"
                            }
                        },
                        "required": ["value"]
                    }
                }
            }
        ])
    print("Assistant created successfully!")
    print("Please, add to .env:")
    print("ASSISTANT_ID=" + assistant.id)