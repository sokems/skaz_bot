from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

menu_main = '🗓 Главное меню'

main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add(menu_main)

menu_admin = ReplyKeyboardMarkup(resize_keyboard=True)
menu_admin_b1 = '📦 Менеджмент МП'
menu_admin_b2 = '🛠 ЦЕХ'
menu_admin.add(menu_admin_b1).add(menu_admin_b2)

back_tseh_menu = ReplyKeyboardMarkup(resize_keyboard=True)
back_tseh_b = '❌ Отмена'
back_tseh_menu.add(back_tseh_b)

tseh_menu = ReplyKeyboardMarkup(resize_keyboard=True)
tseh_menu_b1 = '📋 Табель'
tseh_menu_b2 = '📊 Статистика'
tseh_menu_b3 = '🗣 Предложить'
tseh_menu_b4 = '⭐️ Вакансии'
tseh_menu_b5 = '📕 Инструкции'
tseh_menu.add(tseh_menu_b1).add(tseh_menu_b2, tseh_menu_b4).add(tseh_menu_b3, tseh_menu_b5).add(menu_main)

back_mp_menu = ReplyKeyboardMarkup(resize_keyboard=True)
back_mp_b = '📛 Отмена'
back_mp_menu.add(back_mp_b)

mp_menu = ReplyKeyboardMarkup(resize_keyboard=True)
mp_menu_b1 = '❗️ Непринятые запросы'
mp_menu_b2 = '💊 Личные запросы'
mp_menu_b3 = '💼 Остаток на складе'
mp_menu_b6 = '🚛 Создать доставку'
mp_menu_b7 = '🚀 Список доставок'
mp_menu_b8 = '📦 Отгрузка товаров'
mp_menu_b9 = '⭐️ Отзыв!'
mp_menu.add(mp_menu_b3).add(mp_menu_b8, mp_menu_b9).add(mp_menu_b1, mp_menu_b2).add(mp_menu_b6, mp_menu_b7).add(menu_main)
