"""
Handlers for dialogs with a chatbot based on the OpenAI GPT model.
"""

from aiogram import types
from services.user_service import USER_MODEL_CHOICE, USER_ANALYTICS, ALLOWED_USERS
from datetime import datetime
from services.markups import end_conversation_markup
from services.analytics_service import update_or_add_to_gsheets
from loader import dp
import logging
from services.openai_service import ask_openai
import asyncio

typing_condition = asyncio.Condition()
stop_typing = False
MAX_MESSAGE_LENGTH = 4000


@dp.callback_query_handler(lambda c: c.data in ["gpt3.5", "gpt4"])
async def model_selection(callback_query: types.CallbackQuery):
    """
    Обрабатывает выбор модели пользователем и информирует его о сделанном выборе.

    При получении запроса от пользователя о выборе одной из моделей (GPT-3.5 Turbo или GPT-4), 
    функция сохраняет этот выбор в словаре USER_MODEL_CHOICE и отправляет пользователю сообщение, 
    подтверждающее его выбор. 

    Параметры
    ----------
    callback_query : types.CallbackQuery
        Запрос на колбэк от пользователя, содержащий выбранную им модель.

    Возвращает
    -------
    None

    Примечания
    ----------
    Функция использует глобальную переменную USER_MODEL_CHOICE для сохранения выбора пользователя.
    """
    logging.info("Entered model_selection handler")
    user_id = callback_query.from_user.id
    model = "GPT-3.5 Turbo" if callback_query.data == "gpt3.5" else "GPT-4"
    USER_MODEL_CHOICE[user_id] = {"model": model, "history": ""}
    await dp.bot.answer_callback_query(callback_query.id)
    await dp.bot.send_message(user_id, f"Вы выбрали {model}. Напишите ваше сообщение для начала диалога.")

@dp.message_handler(lambda message: message.from_user.id in USER_MODEL_CHOICE and message.text != '❌ Завершить диалог')
async def process_model_dialog(message: types.Message):
    """
    Обрабатывает сообщения пользователя, взаимодействует с API OpenAI и предоставляет ответ.

    Параметры:
    ----------
    message : types.Message
        Входящее сообщение от пользователя.

    Примечание:
    ----------
    Для взаимодействия с OpenAI использует глобальную переменную USER_MODEL_CHOICE, 
    чтобы отслеживать текущий выбор модели и историю диалога для каждого пользователя.
    """
    user_id = message.from_user.id
    model_data = USER_MODEL_CHOICE[user_id]
    model = model_data['model']
    model_name = "gpt-3.5-turbo-16k" if model == "GPT-3.5 Turbo" else "gpt-4"
    model_data["history"] += f"User: {message.text}\n"
    model_data["history"] = truncate_history(model_data["history"])
    prompt = model_data["history"]

    global stop_typing
    stop_typing = False
    
    # Запускаем анимацию
    typing_task = asyncio.create_task(animate_typing(message))
    await dp.bot.send_chat_action(message.chat.id, action="typing")
    response_text, tokens_used = await ask_openai(model_name, prompt) 
    stop_typing = True
    await typing_task
    model_data["history"] += f"Bot: {response_text}\n"
    current_date = datetime.now().strftime('%Y-%m-%d')
    if user_id not in USER_ANALYTICS:
        USER_ANALYTICS[user_id] = {}
    if current_date not in USER_ANALYTICS[user_id]:
        USER_ANALYTICS[user_id][current_date] = {"GPT-3.5 Turbo": 0, "GPT-4": 0}
    USER_ANALYTICS[user_id][current_date][model] += tokens_used

    user_info = ALLOWED_USERS.get(user_id, {})
    full_name = user_info.get("full_name", "Неизвестный")
    telegram_handle = user_info.get("telegram_handle", "Неизвестный")
    await send_message_in_parts(message.chat.id,response_text,reply_markup=end_conversation_markup)
    await update_or_add_to_gsheets(full_name, telegram_handle, model, tokens_used)

@dp.message_handler(lambda message: message.text == '❌ Завершить диалог' and message.from_user.id in USER_MODEL_CHOICE)
async def end_dialog(message: types.Message):
    """
    Обрабатывает завершение диалога с чат-ботом.

    Параметры:
    ----------
    message : types.Message
        Входящее сообщение от пользователя.
    """
    user_id = message.from_user.id
    if user_id in USER_MODEL_CHOICE:
        del USER_MODEL_CHOICE[user_id]
    await message.answer("Диалог завершен. Хотите начать снова? Нажмите /start.", reply_markup=types.ReplyKeyboardRemove())

def truncate_history(history, max_tokens=15500): 
    """
    Усекает историю диалога, чтобы соответствовать указанному лимиту токенов.
    
    Параметры:
    ----------
    history : str
        Текущая история диалога в виде строки.
    
    max_tokens : int, необязательно
        Максимальное количество токенов для усечения.

    Возвращает:
    -------
    str
        Усеченная история диалога.
    """
    # Разбиваем историю на строки
    lines = history.split("\n")
    
    while len(history) > max_tokens:
        # Удаляем старые строки из истории
        lines.pop(0)
        history = "\n".join(lines)
    return history

@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def unknown_input(message: types.Message):
    """
    Отвечает на неизвестные команды или входные данные пользователя.

    Параметры:
    ----------
    message : types.Message
        Входящее сообщение от пользователя.
    """
    response_text = (
        "Я не понимаю эту команду. Нажмите на кнопку начала или используйте /start, чтобы взаимодействовать с ботом. "
    )
    await dp.bot.send_message(message.chat.id, response_text)

async def animate_typing(message: types.Message):
    """
    Имитирует анимацию печати бота для обратной связи с пользователем.
    
    Параметры:
    ----------
    message : types.Message
        Входящее сообщение от пользователя.
    """
    global stop_typing
    animation = ["Бот печатает.", "Бот печатает..", "Бот печатает..."]
    idx = 0
    sent_message = await message.answer(animation[idx])
    
    while not stop_typing:
        idx = (idx + 1) % 3
        await sent_message.edit_text(animation[idx])
        await asyncio.sleep(1)
        
    await sent_message.delete()

async def send_message_in_parts(chat_id, text, reply_markup, delay=1):
    """
    Отправляет длинные сообщения частями, если они превышают максимально допустимую длину сообщения.
    
    Параметры:
    ----------
    chat_id : int
        ID чата, куда нужно отправить сообщение.

    text : str
        Текст сообщения.

    reply_markup : тип ReplyMarkup, необязательно
        Ответная разметка для сообщения.

    delay : int, необязательно
        Задержка между отправкой нескольких частей сообщения.
    """
    parts = [text[i:i+MAX_MESSAGE_LENGTH] for i in range(0, len(text), MAX_MESSAGE_LENGTH)]
    
    for part in parts:
        await dp.bot.send_message(chat_id, part, reply_markup=reply_markup)
        if len(parts) > 1:
            await asyncio.sleep(delay)
