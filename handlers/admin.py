from aiogram import types
from services.user_service import ADMINS
from loader import dp

@dp.callback_query_handler(lambda c: c.data == "show_analytics" and c.from_user.id in ADMINS)
async def admin_show_analytics(callback_query: types.CallbackQuery):
    link = 'https://docs.google.com/spreadsheets/d/19ngGFqHcVOjPZk7Zklj3nEShjG3uk7rSq6xVCi9_Kxs'
    response = f"Аналитика по пользователям:\n\nНаходится по ссылке:\n{link}"
    await dp.bot.send_message(callback_query.from_user.id, response)