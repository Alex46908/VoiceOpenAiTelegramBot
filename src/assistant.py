from config import Settings
from assistant_tools.save_value import save_value
import json

settings = Settings()

class Assistant:
    def __init__(self, open_ai_client, db_manager):
        self.open_ai_client = open_ai_client
        self.assistant_id = settings.assistant.assistant_id
        self.db_manager = db_manager

    async def send_question(self, message_text):
        thread = await self.open_ai_client.beta.threads.create()
        message = await self.open_ai_client.beta.threads.messages.create(
            thread.id,
            role="user",
            content=message_text
        )

        return message, thread

    async def get_answer(self, thread_id, message_id, user_telegram_id):
        run = await self.open_ai_client.beta.threads.runs.create_and_poll(
            thread_id=thread_id,
            assistant_id=self.assistant_id,
            instructions=settings.assistant.instructions
        )

        if run.status == "requires_action":
            tool_outputs = []
            for tool in run.required_action.submit_tool_outputs.tool_calls:
                if tool.function.name == "save_value":
                    tool_output = await save_value(
                        self.open_ai_client,
                        self.db_manager,
                        user_telegram_id,
                        tool.id,
                        json.loads(tool.function.arguments)["value"]
                    )

                    if tool_output:
                        tool_outputs.append(tool_output)
                    else:
                        return settings.assistant.error_message



            if tool_outputs:
                try:
                    run = await self.open_ai_client.beta.threads.runs.submit_tool_outputs_and_poll(
                        thread_id=thread_id,
                        run_id=run.id,
                        tool_outputs=tool_outputs
                    )
                except Exception as e:
                    print("Failed to submit tool outputs:", e)
                    return settings.assistant.error_message
            else:
                return settings.assistant.error_message

        if run.status == "completed":
            answer_message = await self.open_ai_client.beta.threads.messages.list(
                thread_id=thread_id, order="asc", after=message_id)
            answer_message_text = answer_message.data[0].content[0].text.value

            return answer_message_text
        else:
            return settings.assistant.error_message
