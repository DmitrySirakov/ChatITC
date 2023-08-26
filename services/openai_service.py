"""
OpenAI service module.
Handles operations related to OpenAI requests.
"""

import openai
import asyncio

async def ask_openai(model_name, prompt):
    """
    Запрос к модели OpenAI с заданным запросом (prompt).

    Функция асинхронно запрашивает модель OpenAI с помощью заданного запроса и возвращает ответ от модели,
    а также количество использованных токенов.

    Параметры
    ----------
    model_name : str
        Имя модели OpenAI, к которой следует обратиться.
    prompt : str
        Запрос, который будет передан модели.

    Возвращает
    -------
    str
        Ответ от модели.
    int
        Количество использованных токенов для ответа.

    Исключения
    ----------
    Exception
        В случае ошибки при запросе к OpenAI возвращается сообщение "Ошибка OpenAI" и 0 в качестве количества токенов.

    Примечания
    ----------
    Функция использует синхронный запрос к OpenAI, выполняемый в асинхронном режиме с помощью asyncio.
    """
    loop = asyncio.get_event_loop()
    
    def synchronous_request():
        try:
            response = openai.ChatCompletion.create(
                model=model_name,
                messages=[{'role': 'user', 'content': prompt}]
            )
            return response.choices[0]['message']['content'], response['usage']['completion_tokens']
        except:
            return "Ошибка OpenAI", 0

    return await loop.run_in_executor(None, synchronous_request)
