import logging
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from loader import dp
from aiogram import types
from handlers.start import start
from handlers.dialog import model_selection, process_model_dialog, end_dialog
from handlers.admin import admin_show_analytics
from handlers.help import command_help
from services.user_service import USER_MODEL_CHOICE, ADMINS,update_users_and_admins_periodically
import asyncio

logging.basicConfig(level=logging.INFO)
dp.middleware.setup(LoggingMiddleware())

@dp.message_handler(commands=["start"])
async def on_start(message):
    await start(message)

@dp.callback_query_handler(lambda c: c.data in ["gpt3.5", "gpt4"])
async def on_model_selection(callback_query):
    await model_selection(callback_query)

@dp.message_handler(lambda message: message.from_user.id in USER_MODEL_CHOICE and message.text != '❌ Завершить диалог')
async def on_process_model_dialog(message):
    await process_model_dialog(message)

@dp.message_handler(lambda message: message.text == '❌ Завершить диалог' and message.from_user.id in USER_MODEL_CHOICE)
async def on_end_dialog(message):
    await end_dialog(message)

@dp.callback_query_handler(lambda c: c.data == "show_analytics" and c.from_user.id in ADMINS)
async def on_admin_show_analytics(callback_query):
    await admin_show_analytics(callback_query)

@dp.callback_query_handler(lambda c: c.data == "help")
async def on_help(callback_query):
    await command_help(callback_query)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(update_users_and_admins_periodically())
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)