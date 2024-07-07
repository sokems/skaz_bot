import gspread
# Указываем путь к JSON
gc = gspread.service_account(filename='retail-397705-2cb2125124db.json')
# Открываем тестовую таблицу
sh = gc.open_by_url("https://docs.google.com/spreadsheets/d/1c389riVHBioK2N9elinFl6iqxN_OFTo00EXaipvzN-w")
# Выводим значение ячейки A1
worksheet = sh.worksheet("Расход Август 2023")
# Заменить значение
# worksheet.update('A3', [['Свекла']])

# Значения столбца
values_list = worksheet.col_values(1)
print(values_list)

# Прочитать ячейку
# print(worksheet.get('A3')[0][0])


