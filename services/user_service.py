import csv
from dotenv import load_dotenv
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import asyncio

load_dotenv()
ALLOWED_USERS = {}
USER_ANALYTICS = {}
USER_MODEL_CHOICE = {}
ADMINS = []

async def load_users_from_google_sheets(json_file_path, sheet_name):
    # Определяем область доступа к Google Sheets
    try:
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive.file',
            'https://www.googleapis.com/auth/drive'
        ]

        # Аутентификация и инициализация клиента
        creds = ServiceAccountCredentials.from_json_keyfile_name(json_file_path, scope)
        client = gspread.authorize(creds)

        # Открываем таблицу по имени
        sheet = client.open(sheet_name).sheet1

        # Пропускаем заголовок (первую строку)
        rows = sheet.get_all_values()[1:]
        
        for row in rows:
            user_id, full_name, telegram_handle = row
            ALLOWED_USERS[int(user_id)] = {"full_name": full_name, "telegram_handle": telegram_handle}
    except Exception as e:
        print(f"Error updating from Google Sheets: {e}")

async def load_admins_from_google_sheets(json_file_path, sheet_name):
    global ADMINS
    try:
        # Аутентификация и инициализация клиента, как и в предыдущей функции
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive.file',
            'https://www.googleapis.com/auth/drive'
        ]

        creds = ServiceAccountCredentials.from_json_keyfile_name(json_file_path, scope)
        client = gspread.authorize(creds)
        sheet = client.open(sheet_name).sheet1

        # Загрузка админов
        rows = sheet.get_all_values()[1:]  # Пропускаем заголовок
        new_admins = [int(row[0]) for row in rows if row[0].isdigit()]

        # Если есть изменения, обновляем глобальный список
        if set(new_admins) != set(ADMINS):
            ADMINS = new_admins
            print("Admin list updated!")

    except Exception as e:
        print(f"Error updating admins from Google Sheets: {e}")

async def update_users_and_admins_periodically():
    while True:
        try:
            await load_users_from_google_sheets('dppcommands-7a27921d2259.json', 'Верификация GPT ITC')
            await load_admins_from_google_sheets('dppcommands-7a27921d2259.json', 'Админы GPT ITC')
            await asyncio.sleep(600)  # ждем 10 минут перед следующим обновлением
        except Exception as e:
            print(f"Error during periodic update: {e}")
            await asyncio.sleep(60)  # Если произошла ошибка, попробуем обновиться через минуту
