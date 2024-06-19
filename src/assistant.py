from config import Settings

settings = Settings()

async def init(open_ai_client):
    assistant = await open_ai_client.beta.assistants.create(
        model=settings.assistant.model
    )

    return assistant

async def send_question(open_ai_client, message_text):
    thread = await open_ai_client.beta.threads.create()
    message = await open_ai_client.beta.threads.messages.create(
        thread.id,
        role="user",
        content=message_text
    )

    return message, thread

async def get_answer(open_ai_client, assistant_id, thread_id, message_id):
    await open_ai_client.beta.threads.runs.create_and_poll(
        thread_id=thread_id,
        assistant_id=assistant_id,
        instructions=settings.assistant.instructions
    )

    answer_message = await open_ai_client.beta.threads.messages.list(
        thread_id=thread_id, order="asc", after=message_id)
    answer_message_text = answer_message.data[0].content[0].text.value

    return answer_message_text
