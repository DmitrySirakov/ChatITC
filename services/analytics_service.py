from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

async def update_or_add_to_gsheets(full_name, telegram_handle, model, tokens_used):
    # Открываем Google Sheet
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('dppcommands-7a27921d2259.json', scope)
    client = gspread.authorize(creds)
    sh = client.open('Аналитика GPT ITC')
    worksheet = sh.get_worksheet(0)
    
    # Текущая дата
    current_date = datetime.now().strftime('%Y-%m-%d')

    # Поиск нужной строки по user_id и дате
    cell_list = [cell.strip() for cell in worksheet.col_values(1)]  # получаем все значения из столбца A и убираем пробелы

    # Поиск строки пользователя в таблице
    for index, cell_value in enumerate(cell_list, start=1):  # enumerate начинается с 1 для совпадения с номером строки
        if cell_value == full_name.strip():
            if worksheet.cell(index, 3).value == current_date:
                row_num = index
                break
    else:
        # Находим первую пустую строку или добавляем новую
        row_num = cell_list.index('') if '' in cell_list else len(cell_list) + 1

    # Записываем или обновляем данные
    worksheet.update_acell(f"A{row_num}", full_name)
    worksheet.update_acell(f"B{row_num}", telegram_handle)
    worksheet.update_acell(f"C{row_num}", current_date)
    if worksheet.cell(row_num, 4).value is None:
        tokens_gpt35 = 0
        tokens_gpt4 = 0
    else:
        tokens_gpt35 = float(worksheet.cell(row_num, 4).value.replace(',', '.')) or 0
        tokens_gpt4 = float(worksheet.cell(row_num, 5).value.replace(',', '.')) or 0
    
    if model == "GPT-3.5 Turbo":
        tokens_gpt35 += tokens_used
    else:
        tokens_gpt4 += tokens_used

    worksheet.update_acell(f"D{row_num}", tokens_gpt35)
    worksheet.update_acell(f"E{row_num}", tokens_gpt4)
    cost = (tokens_gpt35 * 0.004/1000) + (tokens_gpt4 * 0.012/1000)
    worksheet.update_acell(f"F{row_num}", cost)