import json
import asyncio

from config import Settings
from assistant_tools.save_value import save_value
from user_thread import UserThread

settings = Settings()

class Assistant:
    def __init__(self, open_ai_client, db_manager):
        self.open_ai_client = open_ai_client
        self.assistant_id = settings.assistant.assistant_id
        self.db_manager = db_manager
        asyncio.run(self._update_assistant())

    async def _update_assistant(self):
        await self.open_ai_client.beta.assistants.update(
            assistant_id=self.assistant_id,
            tool_resources={
                "file_search": {
                    "vector_store_ids": [settings.assistant.vector_storage_id]
                }
            }
        )

    async def send_question(self, message_text, state):

        data = await state.get_data()
        thread_id = data.get('thread_id')

        if thread_id == None:
            thread = await self.open_ai_client.beta.threads.create(
                tool_resources={
                    "file_search": {
                    "vector_store_ids": [settings.assistant.vector_storage_id],
                    }
                }
            )
            thread_id = thread.id
            await state.set_state(UserThread.thread_id)
            await state.update_data(thread_id=thread.id)

        message = await self.open_ai_client.beta.threads.messages.create(
            thread_id,
            role="user",
            content=message_text
        )

        return message, thread_id

    async def get_answer(self, thread_id, message_id, user_telegram_id, statistic_controller):
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
                        statistic_controller.add_event("Успешно сохранена ценность пользователя", str(user_telegram_id))
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

            if len(answer_message.data[0].content[0].text.annotations) != 0:
                annotation = answer_message.data[0].content[0].text.annotations[0]
                file_citation = getattr(annotation, "file_citation", None)

                if file_citation:
                    cited_file = await self.open_ai_client.files.retrieve(file_citation.file_id)
                    answer_message_text += "Взято из файла " + cited_file.filename

            return answer_message_text
        else:
            return settings.assistant.error_message
