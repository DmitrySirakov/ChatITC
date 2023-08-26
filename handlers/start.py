"""
Start Command Handler module.
Handles the /start command in the Telegram bot.
"""

from aiogram import types
from services.markups import get_model_choice_markup
from services.user_service import ALLOWED_USERS
from loader import dp

ADMIN_HANDLE = "@Shadekss"

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    """
    Обработчик команды /start.

    При получении команды /start бот проверяет, разрешен ли доступ пользователю. Если пользователь разрешен,
    отображается клавиатура с выбором модели. В противном случае пользователь уведомляется о отсутствии доступа.

    Параметры
    ----------
    message : types.Message
        Сообщение от пользователя, содержащее команду /start.

    Возвращает
    -------
    None

    Примечания
    ----------
    Функция использует глобальную переменную `ALLOWED_USERS` для проверки прав пользователя.
    Также функция использует глобальную переменную `ADMIN_HANDLE` для вывода контактов администратора при отказе в доступе.
    """
    user_id = message.from_user.id
    if user_id in ALLOWED_USERS:
        user_info = ALLOWED_USERS[user_id]
        full_name = user_info.get("full_name", "Неизвестный")

        markup = get_model_choice_markup(user_id)
        await message.answer(f"Добро пожаловать, {full_name}! Выберите модель для диалога:", reply_markup=markup)
    else:
        await message.answer(f"Извините, у вас нет доступа к этому боту. Пожалуйста, свяжитесь с администратором: {ADMIN_HANDLE}")
