"""
User service module.
Handles operations related to users, including loading them from Google Sheets.
"""

import asyncio
from dotenv import load_dotenv
import gspread
from oauth2client.service_account import ServiceAccountCredentials

load_dotenv()

ALLOWED_USERS = {}
USER_ANALYTICS = {}
USER_MODEL_CHOICE = {}
ADMINS = []

async def load_users_from_google_sheets(json_file_path, sheet_name):
    """
    Асинхронная загрузка и обновление пользователей из Google Таблиц.

    Функция считывает данные пользователей из указанной Google Таблицы и обновляет глобальный словарь ALLOWED_USERS.
    Ожидается, что в таблице три столбца: user_id, full_name и telegram_handle, именно в таком порядке. 
    Первая строка таблицы, как правило заголовок, пропускается.

    Параметры
    ----------
    json_file_path : str
        Путь к JSON-файлу с учетными данными служебной учетной записи, необходимыми для доступа к API Google Таблиц.
    sheet_name : str
        Имя Google Таблицы, из которой следует загрузить данные пользователя.

    Возвращает
    -------
    None

    Исключения
    ----------
    Exception
        Если при доступе к Google Таблицам или обработке данных возникает какая-либо ошибка, сообщение об ошибке выводится.

    Примечания
    ----------
    Требуются библиотеки `gspread` и `oauth2client.service_account`.
    Глобальный словарь `ALLOWED_USERS` обновляется информацией о пользователе, где ключ - это user_id (в виде int),
    а значение - это словарь, содержащий "full_name" и "telegram_handle".
    """
    try:
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive.file',
            'https://www.googleapis.com/auth/drive'
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_name(json_file_path, scope)
        client = gspread.authorize(creds)
        sheet = client.open(sheet_name).sheet1
        rows = sheet.get_all_values()[1:]
        
        for row in rows:
            user_id, full_name, telegram_handle = row
            ALLOWED_USERS[int(user_id)] = {"full_name": full_name, "telegram_handle": telegram_handle}
    except Exception as exc:
        print(f"Error updating from Google Sheets: {exc}")

async def load_admins_from_google_sheets(json_file_path, sheet_name):
    """
    Асинхронная загрузка и обновление списка администраторов из Google Таблиц.

    Функция считывает данные администраторов из указанной Google Таблицы и обновляет глобальный список ADMINS.
    Ожидается, что в таблице есть столбец с user_id администраторов. Первая строка, как правило заголовок, пропускается.

    Параметры
    ----------
    json_file_path : str
        Путь к JSON-файлу с учетными данными служебной учетной записи, необходимыми для доступа к API Google Таблиц.
    sheet_name : str
        Имя Google Таблицы, из которой следует загрузить данные администратора.

    Возвращает
    -------
    None

    Исключения
    ----------
    Exception
        При ошибке при доступе к Google Таблицам или обработке данных выводится сообщение об ошибке.

    Примечания
    ----------
    Функция обновляет глобальную переменную `ADMINS`.
    """
    global ADMINS
    try:
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive.file',
            'https://www.googleapis.com/auth/drive'
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_name(json_file_path, scope)
        client = gspread.authorize(creds)
        sheet = client.open(sheet_name).sheet1
        rows = sheet.get_all_values()[1:]
        new_admins = [int(row[0]) for row in rows if row[0].isdigit()]

        if set(new_admins) != set(ADMINS):
            ADMINS = new_admins
            print("Admin list updated!")
    except Exception as exc:
        print(f"Error updating admins from Google Sheets: {exc}")

async def update_users_and_admins_periodically():
    """
    Периодическое обновление списков пользователей и администраторов из Google Таблиц.

    Функция циклически обновляет списки пользователей и администраторов с интервалом в 10 минут.
    В случае ошибки интервал между попытками сокращается до 1 минуты.

    Возвращает
    -------
    None

    Исключения
    ----------
    Exception
        При ошибке во время периодического обновления выводится сообщение об ошибке.

    Примечания
    ----------
    Функция использует `load_users_from_google_sheets` и `load_admins_from_google_sheets` для загрузки данных.
    """
    while True:
        try:
            await load_users_from_google_sheets('dppcommands-7a27921d2259.json', 'Верификация GPT ITC')
            await load_admins_from_google_sheets('dppcommands-7a27921d2259.json', 'Админы GPT ITC')
            await asyncio.sleep(600)  
        except Exception as exc:
            print(f"Error during periodic update: {exc}")
            await asyncio.sleep(60)
