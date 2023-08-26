"""
Help Command Handler module.
Handles the /help command and its inline query in the Telegram bot.
"""

from aiogram import types
from loader import dp

# Constants for URLs
VERIFICATION_URL = "https://docs.google.com/spreadsheets/d/1A1uDswZcxndNaipcdwBNqkGj3m1X0LUvVCaWG51KJIg/edit#gid=0"
ANALYTICS_URL = "https://docs.google.com/spreadsheets/d/19ngGFqHcVOjPZk7Zklj3nEShjG3uk7rSq6xVCi9_Kxs/edit#gid=0"
ADMIN_ACCESS_URL = "https://docs.google.com/spreadsheets/d/1XfQqr1L40FbD9ysln8wZX6aUtLyhRj7cPL5M4_Xw9ss/edit#gid=0"
ADMIN_HANDLE = "@Shadekss"

@dp.callback_query_handler(lambda c: c.data == "help")
async def command_help(callback_query: types.CallbackQuery):
    """
    Отправляет пользователю подробное сообщение с инструкциями по использованию бота.

    При получении запроса от пользователя на помощь, функция отправляет подробное сообщение, содержащее инструкции
    по взаимодействию с ботом, а также дополнительные ресурсы и контактные данные для администраторов.

    Параметры
    ----------
    callback_query : types.CallbackQuery
        Запрос на колбэк от пользователя, содержащий запрос на помощь.

    Возвращает
    -------
    None

    Примечания
    ----------
    Функция использует глобальные переменные `VERIFICATION_URL`, `ANALYTICS_URL`, `ADMIN_ACCESS_URL` и `ADMIN_HANDLE`
    для формирования текста сообщения с инструкциями.
    """
    help_text = f"""
Привет! Вот инструкции по использованию бота:

/start - Начать диалог с ботом.
Завершить диалог - Окончание текущего диалога.

После выбора модели (GPT-3.5 Turbo или GPT-4), вы можете взаимодействовать с выбранной моделью, отправляя сообщения. 

Для администраторов:
Аналитика - Получить общую статистику использования токенов по датам и выгрузить ее в формате Excel, а также визуалиазация траты токенов по дням.

Верификация пользователей - добавить доступ человеку через эту ссылку:
{VERIFICATION_URL}

Посмотреть аналитику по ссылке(кто сколько по дням потратил, стоимость):
{ANALYTICS_URL}

Выдать доступ администратору:
{ADMIN_ACCESS_URL}

Если у вас возникли проблемы или вопросы, пожалуйста, свяжитесь с {ADMIN_HANDLE}.

Надеемся, вам понравится взаимодействие с нашим ботом!
    """
    await dp.bot.send_message(callback_query.from_user.id, help_text)
