from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from services.user_service import ADMINS

def get_model_choice_markup(user_id):
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
