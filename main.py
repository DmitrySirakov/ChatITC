"""
Main module for bot handlers and execution
"""

import logging
import asyncio
from aiogram import types, executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from loader import dp
from handlers.start import start
from handlers.dialog import model_selection, process_model_dialog, end_dialog
from handlers.admin import admin_show_analytics
from handlers.help import command_help
from services.user_service import (
    USER_MODEL_CHOICE,
    ADMINS,
    update_users_and_admins_periodically
)

logging.basicConfig(level=logging.INFO)
dp.middleware.setup(LoggingMiddleware())

@dp.message_handler(commands=["start"])
async def on_start(message: types.Message):
    """
    Асинхронный обработчик для команды "start".

    Parameters
    ----------
    message : types.Message
        Сообщение от пользователя, которое необходимо обработать.

    Returns
    -------
    Any

    Notes
    -----
    Это обработчик для команды "start". Функция вызывает другую функцию `start`
    для выполнения основных действий.
    """
    await start(message)

@dp.callback_query_handler(lambda c: c.data in ["gpt3.5", "gpt4"])
async def on_model_selection(callback_query: types.CallbackQuery):
    """
    Асинхронный обработчик выбора модели по callback-запросу.

    Обрабатывает выбор пользователя между моделями "gpt3.5" и "gpt4".

    Parameters
    ----------
    callback_query : types.CallbackQuery
        Callback-запрос от пользователя с выбором модели.

    Returns
    -------
    Any

    Notes
    -----
    Этот обработчик активируется при получении callback-запроса, 
    содержащего данные "gpt3.5" или "gpt4". После обработки запроса
    вызывается функция `model_selection` для выполнения соответствующих действий.
    """
    await model_selection(callback_query)


@dp.message_handler(lambda message: message.from_user.id in USER_MODEL_CHOICE and message.text != '❌ Завершить диалог')
async def on_process_model_dialog(message: types.Message):
    """
    Асинхронный обработчик для продолжения диалога модели.

    Обрабатывает сообщения от пользователей, которые ранее выбрали модель 
    и не желают завершать диалог (сообщение отличается от '❌ Завершить диалог').

    Parameters
    ----------
    message : types.Message
        Входящее сообщение от пользователя для продолжения диалога с выбранной моделью.

    Returns
    -------
    Any

    Notes
    -----
    Этот обработчик активируется для пользователей, которые находятся в списке USER_MODEL_CHOICE
    и отправляют сообщение, не равное '❌ Завершить диалог'. После получения сообщения 
    вызывается функция `process_model_dialog` для обработки диалога с выбранной моделью.
    """
    await process_model_dialog(message)

@dp.message_handler(lambda message: message.text == '❌ Завершить диалог' and message.from_user.id in USER_MODEL_CHOICE)
async def on_end_dialog(message: types.Message):
    """
    Асинхронный обработчик для завершения диалога модели.

    Обрабатывает сообщения от пользователей, которые ранее выбрали модель 
    и желают завершить диалог, отправив сообщение '❌ Завершить диалог'.

    Parameters
    ----------
    message : types.Message
        Входящее сообщение от пользователя с желанием завершить диалог.

    Returns
    -------
    Any

    Notes
    -----
    Этот обработчик активируется для пользователей, которые находятся в списке USER_MODEL_CHOICE
    и отправляют сообщение '❌ Завершить диалог'. После получения сообщения вызывается 
    функция `end_dialog` для завершения текущего диалога с выбранной моделью.
    """
    await end_dialog(message)


@dp.callback_query_handler(lambda c: c.data == "show_analytics" and c.from_user.id in ADMINS)
async def on_admin_show_analytics(callback_query: types.CallbackQuery):
    """
    Асинхронный обработчик для показа аналитики администраторам.

    Обрабатывает callback-запросы от администраторов, которые желают просмотреть аналитику,
    отправив запрос с данными "show_analytics".

    Parameters
    ----------
    callback_query : types.CallbackQuery
        Callback-запрос от администратора с желанием просмотреть аналитику.

    Returns
    -------
    Any

    Notes
    -----
    Этот обработчик активируется только для пользователей, которые находятся в списке ADMINS
    и отправляют callback-запрос с данными "show_analytics". После получения запроса 
    вызывается функция `admin_show_analytics` для показа соответствующей аналитики.
    """
    await admin_show_analytics(callback_query)


@dp.callback_query_handler(lambda c: c.data == "help")
async def on_help(callback_query: types.CallbackQuery):
    """
    Асинхронный обработчик для команды помощи.

    Обрабатывает callback-запросы от пользователей, которые отправляют запрос
    с данными "help", с целью получить помощь или инструкции.

    Parameters
    ----------
    callback_query : types.CallbackQuery
        Callback-запрос от пользователя с запросом на помощь.

    Returns
    -------
    Any
        Зависит от функции `command_help`, которая вызывается внутри этой функции.

    Notes
    -----
    При получении callback-запроса с данными "help" вызывается функция `command_help` 
    для предоставления соответствующей информации или инструкций пользователю.
    """
    await command_help(callback_query)


def main():
    """
    Главная функция для запуска бота.

    Инициализирует асинхронный цикл и задачу для периодического обновления пользователей и администраторов.
    Затем начинает опрос с использованием `executor.start_polling`.

    Returns
    -------
    None

    Notes
    -----
    Использует глобальные переменные, такие как `dp` и `executor`, для работы с ботом.
    """
    loop = asyncio.get_event_loop()
    loop.create_task(update_users_and_admins_periodically())
    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    main()
