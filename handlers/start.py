from aiogram import types
from services.markups import get_model_choice_markup
from services.user_service import ALLOWED_USERS
from loader import dp

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    user_id = message.from_user.id
    if user_id in ALLOWED_USERS:
        user_info = ALLOWED_USERS[user_id]
        full_name = user_info.get("full_name", "Неизвестный")

        markup = get_model_choice_markup(user_id)
        await message.answer(f"Добро пожаловать, {full_name}! Выберите модель для диалога:", reply_markup=markup)
    else:
        await message.answer("Извините, у вас нет доступа к этому боту. Пожалуйста, свяжитесь с администратором: @Shadekss")