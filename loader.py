from aiogram import Bot, Dispatcher
import openai
from config import TOKEN, OPENAI_API_KEY
import asyncio
from services.user_service import load_users_from_google_sheets, load_admins_from_google_sheets
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
openai.api_key = OPENAI_API_KEY
loop = asyncio.get_event_loop()

# Загружаем пользователей и админов перед началом работы бота
loop.run_until_complete(load_users_from_google_sheets('dppcommands-7a27921d2259.json', 'Верификация GPT ITC'))
loop.run_until_complete(load_admins_from_google_sheets('dppcommands-7a27921d2259.json', 'Админы GPT ITC'))
