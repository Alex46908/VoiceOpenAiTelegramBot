import time

def init(open_ai_client):
    assistant = open_ai_client.beta.assistants.create(
        model="gpt-4o"
    )
    thread = open_ai_client.beta.threads.create()

    return assistant, thread

def send_question(open_ai_client, thread_id, message_text):
    message = open_ai_client.beta.threads.messages.create(
        thread_id,
        role="user",
        content=message_text
    )

    return message

def get_answer(open_ai_client, assistant_id, thread_id, message_id):
    run = open_ai_client.beta.threads.runs.create_and_poll(
        thread_id=thread_id,
        assistant_id=assistant_id,
        instructions="Please speak with user"
    )
    while run.status == "queued" or run.status == "in_progress":
        run = open_ai_client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id,
        )
        time.sleep(0.3)
    answer_message = open_ai_client.beta.threads.messages.list(
        thread_id=thread_id, order="asc", after=message_id)
    answer_message_text = answer_message.data[0].content[0].text.value

    return answer_message_text
