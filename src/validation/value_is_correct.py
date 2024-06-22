async def value_is_correct(open_ai_client, value, old_values):
    system_content =  "Ответь True, если слова пользователя могут быть его жизенной ценностью, если нет скажи False."
    if old_values is not None:
        system_content = system_content + f"Если слова пользователя синонимичны чему-либо из спсика ({old_values}) скажи False."
    response = await open_ai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system",
             "content": system_content},
            {"role": "user", "content": value}
        ]
    )

    return response.choices[0].message.content == "True"