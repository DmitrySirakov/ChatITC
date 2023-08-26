"""
Admin handlers for interacting with administrative functionalities, such as viewing analytics.
"""

from aiogram import types
from services.user_service import ADMINS
from loader import dp

@dp.callback_query_handler(lambda c: c.data == "show_analytics" and c.from_user.id in ADMINS)
async def admin_show_analytics(callback_query: types.CallbackQuery):
    """
    Обрабатывает запрос администратора на просмотр аналитики пользователей.
    
    Отправляет ссылку на документ Google Sheets, содержащий аналитику пользователей.
    
    Параметры:
    ----------
    callback_query : types.CallbackQuery
        Запрос обратного вызова, содержащий запрос администратора.
    """