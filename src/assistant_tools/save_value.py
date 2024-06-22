import json
from validation.value_is_correct import value_is_correct

async def save_value(open_ai_client, db_manager, user_telegram_id, tool_id, value):
    old_values = await db_manager.find_values(user_telegram_id)

    is_correct = await value_is_correct(open_ai_client, value, old_values)

    if is_correct:
        if old_values is None:
            await db_manager.insert_values(user_telegram_id, value)
        else:
            await db_manager.update_values(user_telegram_id, old_values, value)

        tool_output = {
            "tool_call_id": tool_id,
            "output": ""
        }

        return tool_output

    return \
        {
            "tool_call_id": tool_id,
            "output": "False"
        }