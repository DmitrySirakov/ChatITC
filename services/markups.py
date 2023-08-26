"""
Markups module.
Contains keyboard markup utilities for the bot's user interface.
"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from services.user_service import ADMINS

def get_model_choice_markup(user_id):
    """
    Создаёт и возвращает клавиатуру выбора модели на основе прав пользователя.
    
    Пользователям с административными правами добавляется дополнительная кнопка для аналитики.

    Параметры
    ----------
    user_id : int
        ID пользователя, для которого создается клавиатура.

    Возвращает
    -------
    InlineKeyboardMarkup
        Клавиатура с кнопками для выбора модели и, при наличии прав админа, кнопкой для просмотра аналитики.

    Примечания
    ----------
    Функция использует глобальную переменную `ADMINS` для определения прав пользователя.
    """
    markup = InlineKeyboardMarkup().row(
        InlineKeyboardButton("🤖 GPT-3.5 Turbo", callback_data="gpt3.5"),
        InlineKeyboardButton("🚀 GPT-4", callback_data="gpt4"),
        InlineKeyboardButton("❓ Помощь", callback_data="help")
    )
    # Добавить кнопку аналитики для админов
    if user_id in ADMINS:
        markup.add(InlineKeyboardButton("📊 Аналитика", callback_data="show_analytics"))
    
    return markup
    
end_conversation_markup = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('❌ Завершить диалог')
)
