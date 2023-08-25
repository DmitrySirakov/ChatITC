import openai
import asyncio

async def ask_openai(model_name, prompt):
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
