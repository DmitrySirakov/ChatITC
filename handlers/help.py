from aiogram import types
from loader import dp

dp.callback_query_handler(lambda c: c.data == "help")
async def command_help(callback_query: types.CallbackQuery):
    help_text = """
Привет! Вот инструкции по использованию бота:

/start - Начать диалог с ботом.
Завершить диалог - Окончание текущего диалога.

После выбора модели (GPT-3.5 Turbo или GPT-4), вы можете взаимодействовать с выбранной моделью, отправляя сообщения. 

Для администраторов:
Аналитика - Получить общую статистику использования токенов по датам и выгрузить ее в формате Excel, а также визуалиазация траты токенов по дням.

Верификация пользователей - добавить доступ человеку через эту ссылку:
https://docs.google.com/spreadsheets/d/1A1uDswZcxndNaipcdwBNqkGj3m1X0LUvVCaWG51KJIg/edit#gid=0

Посмотреть аналитику по ссылке(кто сколько по дням потратил, стоимость):
https://docs.google.com/spreadsheets/d/19ngGFqHcVOjPZk7Zklj3nEShjG3uk7rSq6xVCi9_Kxs/edit#gid=0

Выдать доступ администратору:
https://docs.google.com/spreadsheets/d/1XfQqr1L40FbD9ysln8wZX6aUtLyhRj7cPL5M4_Xw9ss/edit#gid=0

Если у вас возникли проблемы или вопросы, пожалуйста, свяжитесь с @Shadekss.

Надеемся, вам понравится взаимодействие с нашим ботом!
    """
    await dp.bot.send_message(callback_query.from_user.id, help_text)


