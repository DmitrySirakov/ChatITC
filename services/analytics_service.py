"""
Analytics Service module.
Handles operations related to analytics data updates in Google Sheets.
"""

from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Constants
SCOPE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]
JSON_FILE_PATH = 'dppcommands-7a27921d2259.json'
SHEET_NAME = 'Аналитика GPT ITC'
TOKEN_COSTS = {
    "GPT-3.5 Turbo": 0.004/1000,
    "GPT-4": 0.012/1000
}

async def update_or_add_to_gsheets(full_name, telegram_handle, model, tokens_used):
    """
    Обновление или добавление данных аналитики в Google Таблицы.

    Функция обновляет или добавляет данные пользователя в Google Таблицы. Если пользователь с такими данными
    и датой уже существует, обновляются данные этого пользователя. В противном случае данные добавляются в
    новую строку.

    Параметры
    ----------
    full_name : str
        Полное имя пользователя.
    telegram_handle : str
        Идентификатор пользователя в Telegram.
    model : str
        Имя модели, которую использовал пользователь ("GPT-3.5 Turbo" или другая).
    tokens_used : float
        Количество использованных токенов при запросе к модели.

    Возвращает
    -------
    None

    Примечания
    ----------
    Для доступа к Google Таблицам функция использует глобальные переменные `JSON_FILE_PATH`, `SCOPE` и `SHEET_NAME`.
    Также функция использует глобальный словарь `TOKEN_COSTS` для расчета стоимости использованных токенов.
    """
    # Setup Google Sheet client
    creds = ServiceAccountCredentials.from_json_keyfile_name(JSON_FILE_PATH, SCOPE)
    client = gspread.authorize(creds)
    worksheet = client.open(SHEET_NAME).get_worksheet(0)

    # Current date
    current_date = datetime.now().strftime('%Y-%m-%d')

    # Find the row with matching user details
    cell_list = [cell.strip() for cell in worksheet.col_values(1)]
    for index, cell_value in enumerate(cell_list, start=1):
        if cell_value == full_name.strip() and worksheet.cell(index, 3).value == current_date:
            row_num = index
            break
    else:
        row_num = cell_list.index('') if '' in cell_list else len(cell_list) + 1

    # Update or set data
    worksheet.update(f"A{row_num}:C{row_num}", [[full_name, telegram_handle, current_date]])

    tokens_gpt35 = float(worksheet.cell(row_num, 4).value.replace(',', '.')) or 0
    tokens_gpt4 = float(worksheet.cell(row_num, 5).value.replace(',', '.')) or 0

    if model == "GPT-3.5 Turbo":
        tokens_gpt35 += tokens_used
    else:
        tokens_gpt4 += tokens_used

    cost = (tokens_gpt35 * TOKEN_COSTS["GPT-3.5 Turbo"]) + (tokens_gpt4 * TOKEN_COSTS["GPT-4"])
    
    worksheet.update(f"D{row_num}:F{row_num}", [[tokens_gpt35, tokens_gpt4, cost]])
