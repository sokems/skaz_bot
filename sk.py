from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import time
import pymysql
from config import host, user_name, password, db_name
import re
from openpyxl import load_workbook
import gspread
import datetime

gc = gspread.service_account(filename='retail-397705-2cb2125124db.json')
sh = gc.open_by_url("https://docs.google.com/spreadsheets/d/1c389riVHBioK2N9elinFl6iqxN_OFTo00EXaipvzN-w")

def update(text, user):
    try:
        connection = pymysql.connect(
            host=host,
            port=3306,
            user=user_name,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )

        try:
            with connection.cursor() as cursor:
                cursor.execute(text)
                connection.commit()
                return 0

        finally:
            connection.close()
    except Exception as ex:
        return f'Ошибка {ex}. Не продолжайте!\n\nПередайте руководителю и нажмите <b>ОТМЕНА</b>'

def create(text, user):
    try:
        connection = pymysql.connect(
            host=host,
            port=3306,
            user=user_name,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )

        try:
            with connection.cursor() as cursor:
                cursor.execute(text)
                connection.commit()
                return 0

        finally:
            connection.close()
    except Exception as ex:
        return f'Ошибка {ex}. Не продолжайте!\n\nПередайте руководителю и нажмите <b>ОТМЕНА</b>'

def selone(text, user):
    try:
        connection = pymysql.connect(
            host=host,
            port=3306,
            user=user_name,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )

        try:
            with connection.cursor() as cursor:
                cursor.execute(text)
                return cursor.fetchone()

        finally:
            connection.close()
    except Exception as ex:
        return f'Ошибка {ex}. Не продолжайте!\n\nПередайте руководителю и нажмите <b>ОТМЕНА</b>'

def selist(text, user):
    try:
        connection = pymysql.connect(
            host=host,
            port=3306,
            user=user_name,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )

        try:
            with connection.cursor() as cursor:
                cursor.execute(text)
                return cursor.fetchall()

        finally:
            connection.close()
    except Exception as ex:
        return f'Ошибка {ex}. Не продолжайте!\n\nПередайте руководителю и нажмите <b>ОТМЕНА</b>'

def defaul_values(id_user):
    try:
        connection = pymysql.connect(
            host=host,
            port=3306,
            user=user_name,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )

        try:
            with connection.cursor() as cur:
                cur.execute(f"UPDATE users SET word_5 = ' ', calc_box = 0, price = 0, height = 0, height_flag = 0, length1 = 0, "
                            f"length_flag = 0, width = 0, width_flag = 0, min_price = 0, minus_item2 = 0, "
                            f"xl_ul = 0, xl_ul_text = '', xl_tel = 0, xl_tel_text = 0, xl_type = 0, "
                            f"xl_type_text = '', xl_count_type = 0, xl_count_type_text = 0, xl_mark = 0, "
                            f"xl_mark_text = '', xl_pack = 0, xl_pack_text = '', xl_comment = 0, "
                            f"xl_comment_text = '', xl_city = 0, xl_city_text = '', xl_count_box = 0, "
                            f"xl_count_box_text = 0, xl_count_items = 0, xl_count_items_text = '', "
                            f"xl_comment_city = 0, xl_comment_city_text = '', xl_markbox = 0, xl_markbox_text = '', "
                            f"logistic = 0, ff = 0, new_id_user = 0, new_id_user_text = '', new_name_user = 0, "
                            f"remove_user = 0, fbo_15 = 0, new_car_city = 0, new_car_plan_start = 0, "
                            f"new_car_plan_end = 0, car_drive = 0, num_car = 0, drive_num = 0, gate = 0, "
                            f"find_car = 0, car_city = 0, chcar = 0, del_car = 0, find_zakaz = 0, sumpd = 0, "
                            f"countpd = 0, text_user = 0, id_fbo = 0, new_car_city_text = '', zak_day = 0, "
                            f"zak_mon = 0, zak_year = 0, ef_day = 0, ef_mon = 0, ef_year = 0, zabor = 0, "
                            f"ed_day = 0, ed_mon = 0, ed_year = 0, prib_day = 0, prib_mon = 0, prib_year = 0, "
                            f"fbo_16 = 0, chcar_2 = 0, remove_user_adm = 0, fbo_11 = 0, fbo_18 = 0, fbo_18_1 = 0, "
                            f"gate_2 = 0, find_car = 0, find_car_4 = 0, weight = 0, count_pal_flag = 0, "
                            f"max_id_item = 0, add_set_0 = 0, add_set_1 = 0, add_set_4 = 0, "
                            f"add_set_5 = 0, add_set_6 = 0, add_set_7 = 0, add_set_8 = 0, add_set_9 = 0, "
                            f"add_set_10 = 0, add_set_11 = 0, add_set_12 = 0, add_set_13 = 0, find_item = 0, "
                            f"what_in_box = 0, choose_ul = '', edit_item = 0, all_edit_item = 0, choose_id = '', "
                            f"choose_pr = '', edit_pr = 0, add_ul = 0, plus_new_sell = 0, plus_new_sell2 = 0, "
                            f"plus_new_sell3 = 0, count_wb = 0, count_ozon = 0, edit_box = 0, edit_box_item = 0, "
                            f"choose_box = '', edit_box_item_add = 0, find_item_id = 0, edit_ul_2 = 0, "
                            f"new_id_user = 0, new_id_user_text = '', new_name_user = 0, remove_user = 0, "
                            f"plus_new_sell4 = 0, text_user = 0, count_wb_60 = 0, count_ozon_60 = 0, "
                            f"count_wb_120 = 0, count_ozon_120 = 0, count_wb_max = 0, count_ozon_max = 0, "
                            f"plus_new_sell5 = 0, plus_new_sell6 = 0, plus_new_sell7 = 0, plus_new_sell8 = 0, "
                            f"plus_new_sell9 = 0, remove_user_adm = 0, find_item2 = 0, choose_ul_id = 0, act_sk = ' ' WHERE id_user = '{id_user}'")
                connection.commit()
                return 0

        finally:
            connection.close()
    except Exception as ex:
        return f'Ошибка {ex}. Не продолжайте!\n\nПередайте руководителю и нажмите <b>ОТМЕНА</b>'

def sklad(user, name_obj, otk, kud, kol):
    delta_1 = datetime.timedelta(hours=5)
    now = datetime.datetime.now() + delta_1
    if int(now.day) < 10:
        day_edit = '0' + str(now.day)
    else:
        day_edit = now.day

    if int(now.month) < 10:
        month_edit = '0' + str(now.month)
    else:
        month_edit = now.month

    if int(now.hour) < 10:
        hour_edit = '0' + str(now.hour)
    else:
        hour_edit = now.hour

    if int(now.minute) < 10:
        minute_edit = '0' + str(now.minute)
    else:
        minute_edit = now.minute

    if now.month == 1:
        name_list = f"Движение склад Январь {now.year}"
    elif now.month == 2:
        name_list = f"Движение склад Февраль {now.year}"
    elif now.month == 3:
        name_list = f"Движение склад Март {now.year}"
    elif now.month == 4:
        name_list = f"Движение склад Апрель {now.year}"
    elif now.month == 5:
        name_list = f"Движение склад Май {now.year}"
    elif now.month == 6:
        name_list = f"Движение склад Июнь {now.year}"
    elif now.month == 7:
        name_list = f"Движение склад Июль {now.year}"
    elif now.month == 8:
        name_list = f"Движение склад Август {now.year}"
    elif now.month == 9:
        name_list = f"Движение склад Сентябрь {now.year}"
    elif now.month == 10:
        name_list = f"Движение склад Октябрь {now.year}"
    elif now.month == 11:
        name_list = f"Движение склад Ноябрь {now.year}"
    elif now.month == 12:
        name_list = f"Движение склад Декабрь {now.year}"



    date_create = f'{hour_edit}:{minute_edit} - {day_edit}.{month_edit}.{now.year}'
    user_name = selone(f"SELECT name_user FROM users WHERE id_user = '{user}'", user)['name_user']

    worksheet = sh.worksheet(name_list)
    values_list = worksheet.col_values(1)
    num_row = len(values_list) + 1

    worksheet.update_cell(num_row, 1, date_create)
    worksheet.update_cell(num_row, 11, name_obj)
    worksheet.update_cell(num_row, 18, otk)
    worksheet.update_cell(num_row, 23, kud)
    worksheet.update_cell(num_row, 28, kol)
    worksheet.update_cell(num_row, 32, user_name)

def date_create():
    delta_1 = datetime.timedelta(hours=5)
    now = datetime.datetime.now() + delta_1
    if int(now.day) < 10:
        day_edit = '0' + str(now.day)
    else:
        day_edit = now.day

    if int(now.month) < 10:
        month_edit = '0' + str(now.month)
    else:
        month_edit = now.month

    res = f'{day_edit}.{month_edit}.{now.year}'

    return res

def date_tomorrow_create():
    delta_1 = datetime.timedelta(days=1)
    now = datetime.datetime.now() + delta_1

    if int(now.day) < 10:
        day_edit = '0' + str(now.day)
    else:
        day_edit = now.day

    if int(now.month) < 10:
        month_edit = '0' + str(now.month)
    else:
        month_edit = now.month

    res = f'{day_edit}.{month_edit}.{now.year}'

    return res

def date_and_time_create():
    delta_1 = datetime.timedelta(hours=5)
    now = datetime.datetime.now() + delta_1
    if int(now.day) < 10:
        day_edit = '0' + str(now.day)
    else:
        day_edit = now.day

    if int(now.month) < 10:
        month_edit = '0' + str(now.month)
    else:
        month_edit = now.month

    if int(now.hour) < 10:
        hour_edit = '0' + str(now.hour)
    else:
        hour_edit = now.hour

    if int(now.minute) < 10:
        minute_edit = '0' + str(now.minute)
    else:
        minute_edit = now.minute

    res = f'{hour_edit}:{minute_edit} - {day_edit}.{month_edit}.{now.year}'

    return res

def time_create():
    delta_1 = datetime.timedelta(hours=5)
    now = datetime.datetime.now() + delta_1


    if int(now.hour) < 10:
        hour_edit = '0' + str(now.hour)
    else:
        hour_edit = now.hour

    if int(now.minute) < 10:
        minute_edit = '0' + str(now.minute)
    else:
        minute_edit = now.minute

    res = f'{hour_edit}:{minute_edit}'

    return res