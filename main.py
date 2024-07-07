from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import markups
import texts
import time
import pymysql
from config import host, user_name, password, db_name
import re
from openpyxl import load_workbook
import gspread
import datetime
import sk
import json
import aiocron


TOKEN = ''

bot = Bot(TOKEN, parse_mode='Markdown')
db = Dispatcher(bot)

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
                cur.execute(f"UPDATE users SET act_wood = ' ', act_log = ' ' WHERE id_user = '{id_user}'")
                connection.commit()
                return 0

        finally:
            connection.close()
    except Exception as ex:
        return f'Ошибка {ex}. Не продолжайте!\n\nПередайте руководителю и нажмите <b>ОТМЕНА</b>'

async def startup(_):
    print('Бот запущен')

@db.message_handler(content_types=['photo'])
async def handle_docs_photo(message):
    user = message.chat.id
    if user == -1001933713976 or user == -984607796 or user == -1002146643966:
        pass
    elif selone(f"SELECT act_wood FROM users WHERE id_user = '{user}'", user)['act_wood'] == 'otz':
        id_photo = message.photo[-1]['file_id']
        list_users = selist(f"SELECT id_user FROM users WHERE company = 'Сборщик' OR company = 'Мастер' OR company = 'Босс'", user)
        for user1 in list_users:
            try:
                chat_id = str(user1["id_user"])
                await bot.send_photo(chat_id, id_photo, caption='Отзыв покупателя')
            except:
                pass
        await message.answer(
            text='✅ Картинка отправлена!', reply_markup=markups.mp_menu)
    else:
        try:
            if 'Заказа_' in selone(f"SELECT act_wood FROM users WHERE id_user = '{user}'", user)['act_wood']:
                await message.answer(text='Пришлите *QR заказа* документом .pdf!!!!')
            elif 'Поставки_' in selone(f"SELECT act_wood FROM users WHERE id_user = '{user}'", user)['act_wood']:
                await message.answer(text='Пришлите *QR поставки* документом .pdf!!!!')
            else:
                await message.answer(text=message.photo[3].file_id)
        except Exception as e:
            await message.answer(text=e)

@db.message_handler(content_types=['document'])
async def handle_docs_photo(message):
    user = message.chat.id
    if user == -1001933713976 or user == -984607796 or user == -1002146643966:
        pass
    else:
        try:
            if 'Заказа_' in selone(f"SELECT act_wood FROM users WHERE id_user = '{user}'", user)['act_wood']:
                id_sup = selone(f"SELECT act_wood FROM users WHERE id_user = '{user}'", user)['act_wood'].split("_")[1]
                mes = 'Поставки_' + id_sup
                update(f"UPDATE users SET act_wood = '{mes}' WHERE id_user = '{user}'", user)
                file_info = await bot.get_file(message.document.file_id)

                downloaded_file = await bot.download_file(file_info.file_path)
                src = f'zak/' + str(id_sup) + '_1.pdf'
                with open(src, 'wb') as new_file:
                    new_file.write(downloaded_file.getvalue())

                data = open(f'zak/{id_sup}_1.pdf', 'rb')
                await bot.send_document(-1001915163310, document=data)
                data.close()


                await message.answer(text='Пришлите *QR поставки* документом .pdf')
            elif 'Поставки_' in selone(f"SELECT act_wood FROM users WHERE id_user = '{user}'", user)['act_wood']:
                id_sup = selone(f"SELECT act_wood FROM users WHERE id_user = '{user}'", user)['act_wood'].split("_")[1]
                mes = ' '
                update(f"UPDATE users SET act_wood = '{mes}' WHERE id_user = '{user}'", user)
                file_info = await bot.get_file(message.document.file_id)

                downloaded_file = await bot.download_file(file_info.file_path)
                src = f'zak/' + str(id_sup) + '_2.pdf'
                with open(src, 'wb') as new_file:
                    new_file.write(downloaded_file.getvalue())

                data = open(f'zak/{id_sup}_2.pdf', 'rb')
                await bot.send_document(-1001915163310, document=data)
                data.close()

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

                date_report = str(day_edit) + '.' + str(month_edit) + '.' + str(now.year)

                update(f"UPDATE wood SET date_c = '{date_report}' WHERE id_sup = '{id_sup}'", user)
                update(f"UPDATE wood SET status_ship = 'Обрабатывается в цеху' WHERE id_sup = '{id_sup}'", user)

                sup = selist(f"SELECT * FROM wood WHERE id_sup = '{id_sup}'", user)[0]

                list_det = sup['list_det'].split(' ')
                det = ''
                for d in list_det:
                    if d == '1':
                        det += '\nНожка стула'
                    elif d == '2':
                        det += '\nНожка стола'
                    elif d == '3':
                        det += '\nСпинка стула'
                    elif d == '4':
                        det += '\nСидение стула'
                    elif d == '5':
                        det += '\nБоковая планка стула'
                    elif d == '6':
                        det += '\nПеремычка стола'
                    elif d == '7':
                        det += '\nСтолешница в сборе'
                    elif d == '8':
                        det += '\nБоковая планка стола'
                    elif d == '9':
                        det += '\nСтолешница'
                    elif d == '10':
                        det += '\nФурнитура'


                mess = f'Нужно подготовить и отправить детали!' \
                       f'\n*{det}*'


                list_users = selist(f"SELECT id_user FROM users WHERE company = 'Босс' OR company = 'Мастер'", user)
                for user1 in list_users:
                    try:
                        chat_id = str(user1["id_user"])
                        destination_bot = Bot(token='6682205213:AAFFV1avM8cVCZhgv-K8pzKeJ_c20Wle_P4')
                        await destination_bot.send_message(chat_id, mess, parse_mode='Markdown')
                    except:
                        pass

                await message.answer(text='⭐️ Информация передана в цех!', reply_markup=markups.mp_menu)
            else:
                await message.answer(text=message.document.file_id, parse_mode='HTML')
        except Exception as e:
            await message.answer(text=e, parse_mode='HTML')

async def data_base_update():
    await bot.send_message(chat_id='395784406', text='База средств обновляется...', parse_mode='Markdown')
    user = 395784406

    delta_1 = datetime.timedelta(hours=5)
    now = datetime.datetime.now()
    if int(now.day) < 10:
        day_edit = '0' + str(now.day)
    else:
        day_edit = now.day

    if int(now.month) < 10:
        month_edit = '0' + str(now.month)
    else:
        month_edit = now.month

    if now.month == 1:
        name_list = f"График Январь {now.year}"
    elif now.month == 2:
        name_list = f"График Февраль {now.year}"
    elif now.month == 3:
        name_list = f"График Март {now.year}"
    elif now.month == 4:
        name_list = f"График Апрель {now.year}"
    elif now.month == 5:
        name_list = f"График Май {now.year}"
    elif now.month == 6:
        name_list = f"График Июнь {now.year}"
    elif now.month == 7:
        name_list = f"График Июль {now.year}"
    elif now.month == 8:
        name_list = f"График Август {now.year}"
    elif now.month == 9:
        name_list = f"График Сентябрь {now.year}"
    elif now.month == 10:
        name_list = f"График Октябрь {now.year}"
    elif now.month == 11:
        name_list = f"График Ноябрь {now.year}"
    elif now.month == 12:
        name_list = f"График Декабрь {now.year}"

    worksheet = sh.worksheet(name_list)

    id_list_g = worksheet.row_values(35)
    id_list = []
    index_id_list = []
    for i in range(4, len(id_list_g)):
        if len(id_list_g[i]) > 0:
            id_list.append(id_list_g[i])
            index_id_list.append(i + 1)

    for u in index_id_list:
        values_list = ' '.join(worksheet.col_values(u)).encode('utf8').decode('utf8').split(" ")
        id_user = values_list[36]
        name_user = values_list[0] + ' ' + values_list[1]
        team_user = values_list[37] + ' ' + values_list[38]
        hour_user = values_list[39] + ' ' + values_list[40]
        sum_hour_user = values_list[41]
        dop_user = values_list[42] + ' ' + values_list[43]
        sum_dop_user = values_list[44]
        voz_user = values_list[45] + ' ' + values_list[46]
        sum_voz_user = values_list[47]
        night_user = values_list[48]
        raz_user = values_list[49] + ' ' + values_list[50]
        sum_raz_user = values_list[51]
        pay_user = values_list[53]
        main_user = values_list[55]
        need_user = values_list[56]
        shtraf_user = values_list[57]
        prem_user = values_list[58]
        otp = values_list[60] + ' ' + values_list[61]
        otp_sum = values_list[62]

        create(f"REPLACE INTO skaz_users(id_user, name_user, team_user, hour_user, sum_hour_user, dop_user, sum_dop_user, voz_user, sum_voz_user, night_user, raz_user, sum_raz_user, pay_user, main_user, need_user, shtraf, prem, otp, otp_sum) VALUES ('{id_user}', '{name_user}', '{team_user}', '{hour_user}', '{sum_hour_user}', '{dop_user}', '{sum_dop_user}', '{voz_user}', '{sum_voz_user}', '{night_user}', '{raz_user}', '{sum_raz_user}', '{pay_user}', '{main_user}', '{need_user}', '{shtraf_user}', '{prem_user}', '{otp}', '{otp_sum}')", user)


async def data_base_update_2():
    user = 395784406
    delta_1 = datetime.timedelta(hours=5)
    now = datetime.datetime.now()
    if int(now.day) < 10:
        day_edit = '0' + str(now.day)
    else:
        day_edit = now.day

    if int(now.month) < 10:
        month_edit = '0' + str(now.month)
    else:
        month_edit = now.month

    if now.month == 1:
        name_list = f"График Январь {now.year}"
        month = 'Январь 1'
        month_2 = 'Январь 2'
        month_3 = 'Январь 3'
    elif now.month == 2:
        name_list = f"График Февраль {now.year}"
        month = 'Февраль 1'
        month_2 = 'Февраль 2'
        month_3 = 'Февраль 3'
    elif now.month == 3:
        name_list = f"График Март {now.year}"
        month = 'Март 1'
        month_2 = 'Март 2'
        month_3 = 'Март 3'
    elif now.month == 4:
        name_list = f"График Апрель {now.year}"
        month = 'Апрель 1'
        month_2 = 'Апрель 2'
        month_3 = 'Апрель 3'
    elif now.month == 5:
        name_list = f"График Май {now.year}"
        month = 'Май 1'
        month_2 = 'Май 2'
        month_3 = 'Май 3'
    elif now.month == 6:
        name_list = f"График Июнь {now.year}"
        month = 'Июнь 1'
        month_2 = 'Июнь 2'
        month_3 = 'Июнь 3'
    elif now.month == 7:
        name_list = f"График Июль {now.year}"
        month = 'Июль 1'
        month_2 = 'Июль 2'
        month_3 = 'Июль 3'
    elif now.month == 8:
        name_list = f"График Август {now.year}"
        month = 'Август 1'
        month_2 = 'Август 2'
        month_3 = 'Август 3'
    elif now.month == 9:
        name_list = f"График Сентябрь {now.year}"
        month = 'Сентябрь 1'
        month_2 = 'Сентябрь 2'
        month_3 = 'Сентябрь 3'
    elif now.month == 10:
        name_list = f"График Октябрь {now.year}"
        month = 'Октябрь 1'
        month_2 = 'Октябрь 2'
        month_3 = 'Октябрь 3'
    elif now.month == 11:
        name_list = f"График Ноябрь {now.year}"
        month = 'Ноябрь 1'
        month_2 = 'Ноябрь 2'
        month_3 = 'Ноябрь 3'
    elif now.month == 12:
        name_list = f"График Декабрь {now.year}"
        month = 'Декабрь 1'
        month_2 = 'Декабрь 2'
        month_3 = 'Декабрь 3'

    worksheet = sh.worksheet(name_list)

    team_1 = worksheet.row_values(58)
    team_2 = worksheet.row_values(59)
    all_team = worksheet.row_values(58)

    create(f"REPLACE INTO skaz_stat(month, name_team, wood, raz, voz, count_day) VALUES ('{month}', '{team_1[3]}', '{team_1[6]}', '{team_1[10]}', '{team_1[14]}', '{team_1[18]}')", user)
    create(f"REPLACE INTO skaz_stat(month, name_team, wood, raz, voz, count_day) VALUES ('{month_2}', '{team_2[3]}', '{team_2[6]}', '{team_2[10]}', '{team_2[14]}', '{team_2[18]}')", user)
    create(f"REPLACE INTO skaz_stat(month, name_team, wood, raz, voz, count_day) VALUES ('{month_3}', 'Общая статистика', '{int(all_team[34]) - int(all_team[22])}', '{all_team[26]}', '{all_team[30]}', '{all_team[22]}')", user)

    await bot.send_message(chat_id='395784406', text='База средств обновилась!', parse_mode='Markdown')


@aiocron.crontab('0 20 * * *')
async def scheduled_message():
    await data_base_update()
    await data_base_update_2()

@aiocron.crontab('0 5 1 * *')
async def scheduled_message_2():
    user = 395784406
    delta_1 = datetime.timedelta(hours=5)
    now = datetime.datetime.now()
    now_day = str(now.day)
    now_month = int(now.month) - 1

    if now_day == '1':
        if now_month == 1:
            name_list = f"Январь {now.year}"
        elif now_month == 2:
            name_list = f"Февраль {now.year}"
        elif now_month == 3:
            name_list = f"Март {now.year}"
        elif now_month == 4:
            name_list = f"Апрель {now.year}"
        elif now_month == 5:
            name_list = f"Май {now.year}"
        elif now_month == 6:
            name_list = f"Июнь {now.year}"
        elif now_month == 7:
            name_list = f"Июль {now.year}"
        elif now_month == 8:
            name_list = f"Август {now.year}"
        elif now_month == 9:
            name_list = f"Сентябрь {now.year}"
        elif now_month == 10:
            name_list = f"Октябрь {now.year}"
        elif now_month == 11:
            name_list = f"Ноябрь {now.year}"
        elif now_month == 12:
            name_list = f"Декабрь {now.year}"

        list_tab_old = selist(f"SELECT * FROM skaz_users", user)
        for list_tab in list_tab_old:
            await bot.send_message(chat_id= list_tab["id_user"], text=f'ℹ️ Табель сотрудника с номером: *{list_tab["id_user"]}*\n\n'
                                      f'📅 Месяц: *{name_list}*\n'
                                      f'🏷 Имя: *{list_tab["name_user"]}*\n'
                                      f'🎒 Команда: *{list_tab["team_user"]}*\n\n'
                                      f'—————————————————————\n\n'
                                      f'🔨 Отработано:\n'
                                      f'Часов: *{list_tab["hour_user"]}*\n'
                                      f'Сумма по часам: *{list_tab["sum_hour_user"]}*\n\n'
                                      f'🏆 Доп. мотивация:\n'
                                      f'Изделий дополнительно: *{list_tab["dop_user"]}*\n'
                                      f'Сумма: *{list_tab["sum_dop_user"]}*\n\n'
                                      f'💣 Возвраты:\n'
                                      f'Переупаковано: *{list_tab["voz_user"]}*\n'
                                      f'Сумма: *{list_tab["sum_voz_user"]}*\n\n'
                                      f'🌒 Ночные смены:\n'
                                      f'Сумма: *{list_tab["night_user"]}*\n\n'
                                      f'🚛 Разгрузки:\n'
                                      f'Разгружено: *{list_tab["raz_user"]}*\n'
                                      f'Сумма: *{list_tab["sum_raz_user"]}*\n\n'
                                      f'🤑 Премия:\n'
                                      f'Сумма: *{list_tab["prem"]}*\n\n'
                                      f'—————————————————————\n\n'
                                      f'🌴 Дней отпуска: *{list_tab["otp"]}*\n' \
                                      f'💶 Сумма за отпуск: *{list_tab["otp_sum"]}*\n\n' \
                                      f'—————————————————————\n\n' \
                                      f'💰 Общая заработная плата: *{list_tab["main_user"]}*\n\n'
                                      f'💸 Выплачено: *{list_tab["pay_user"]}*\n'
                                      f'⛔️ Штраф: *{list_tab["shtraf"]}*\n\n'
                                      f'—————————————————————\n\n'
                                      f'💵 Будет выплачено: *{list_tab["need_user"]}*\n')

            mess = f'Сотруднику *{list_tab["name_user"]}* сформирован окончательный табель!\n\n' \
                   f'ℹ️ Табель сотрудника с номером: *{list_tab["id_user"]}*\n\n' \
                   f'📅 Месяц: *{name_list}*\n' \
                   f'🏷 Имя: *{list_tab["name_user"]}*\n' \
                   f'🎒 Команда: *{list_tab["team_user"]}*\n\n' \
                   f'—————————————————————\n\n' \
                   f'🔨 Отработано:\n' \
                   f'Часов: *{list_tab["hour_user"]}*\n' \
                   f'Сумма по часам: *{list_tab["sum_hour_user"]}*\n\n' \
                   f'🏆 Доп. мотивация:\n' \
                   f'Изделий дополнительно: *{list_tab["dop_user"]}*\n' \
                   f'Сумма: *{list_tab["sum_dop_user"]}*\n\n' \
                   f'💣 Возвраты:\n' \
                   f'Переупаковано: *{list_tab["voz_user"]}*\n' \
                   f'Сумма: *{list_tab["sum_voz_user"]}*\n\n' \
                   f'🌒 Ночные смены:\n' \
                   f'Сумма: *{list_tab["night_user"]}*\n\n' \
                   f'🚛 Разгрузки:\n' \
                   f'Разгружено: *{list_tab["raz_user"]}*\n' \
                   f'Сумма: *{list_tab["sum_raz_user"]}*\n\n' \
                   f'🤑 Премия:\n' \
                   f'Сумма: *{list_tab["prem"]}*\n\n' \
                   f'—————————————————————\n\n' \
                   f'🌴 Дней отпуска: *{list_tab["otp"]}*\n' \
                   f'💶 Сумма за отпуск: *{list_tab["otp_sum"]}*\n\n' \
                   f'—————————————————————\n\n' \
                   f'💰 Общая заработная плата: *{list_tab["main_user"]}*\n\n' \
                   f'💸 Выплачено: *{list_tab["pay_user"]}*\n' \
                   f'⛔️ Штраф: *{list_tab["shtraf"]}*\n\n' \
                   f'—————————————————————\n\n' \
                   f'💵 Нужно выплатить: *{list_tab["need_user"]}*\n'

            list_users = selist(f"SELECT id_user FROM users WHERE company = 'Босс'", user)
            for user1 in list_users:
                try:
                    chat_id = str(user1["id_user"])
                    destination_bot = Bot(token='6682205213:AAFFV1avM8cVCZhgv-K8pzKeJ_c20Wle_P4')
                    await destination_bot.send_message(chat_id, mess, parse_mode='Markdown')
                except:
                    pass


@db.message_handler(commands='info')
async def info_command(message: types.Message):
    id_user_get = f'`{message.chat.id}`'
    await message.answer(text=id_user_get, parse_mode='Markdown')

@db.message_handler(commands='mes')
async def info_command(message: types.Message):
    user = message.chat.id
    id_sup = 35
    id_doc_1 = selone(f"SELECT id_doc_1 FROM wood WHERE id_sup = '{id_sup}'", user)['id_doc_1']
    await bot.send_document(user, id_doc_1)

@db.message_handler(commands='update')
async def test_command(message: types.Message):
    await data_base_update()
    await data_base_update_2()

@db.message_handler(commands='test')
async def test_command(message: types.Message):
    user = message.chat.id
    delta_1 = datetime.timedelta(days=1)
    delta_2 = datetime.timedelta(hours=5)
    now = datetime.datetime.now() - delta_1 + delta_2

    if int(now.day) < 10:
        day_edit = '0' + str(now.day)
    else:
        day_edit = now.day

    if int(now.month) < 10:
        month_edit = '0' + str(now.month)
    else:
        month_edit = now.month

    date_report = str(day_edit) + '.' + str(month_edit) + '.' + str(now.year)




    list_id = selist(f"SELECT * FROM report_wood WHERE date_report = '{date_report}'", user)
    worksheet = sh.worksheet("Заказы маркетплейс 2024")
    # выгружаем строку МП
    mp_list = worksheet.row_values(2)

    # поиск номера строки с датой
    find_row = worksheet.find(date_report).row

    for item in list_id:
        find_col = 0
        id_item = item["id_item"]
        list_item = selist(f"SELECT * FROM price_wood WHERE id_item = '{id_item}'", user)[0]
        name_item = list_item['name_item'].split('_')[0]
        ul_item = list_item['name_item'].split('_')[1]
        mp_item = list_item['name_item'].split('_')[2]
        price_item = list_item['price_item']
        count_item = item["count_item"]

        # поиск ячейки с названием позиции
        cell = worksheet.find(name_item)

        # поиск номера столбца МП по позиции
        for mp in range(cell.col - 1, len(mp_list)):
            # поиск номера столбца ЮЛ по позиции
            if mp_list[mp] == mp_item:
                if ul_item == 'ООО РИТЕЙЛ ПЛЮС':
                    find_col = mp + 1
                    break
                elif ul_item == 'ИП КАЛИМУЛЛИН':
                    find_col = mp + 4
                    break

        # номер стоблца кол-во по экселю
        count_col = find_col

        # номер стоблца цена по экселю
        price_col = find_col + 1

        # Обновляем ячейки
        worksheet.update_cell(find_row, count_col, count_item)
        worksheet.update_cell(find_row, price_col, price_item)

        await message.answer(text=f'{name_item} {ul_item} {mp_item} ({find_row};{find_col})',
                             reply_markup=markups.mp_menu, parse_mode='HTML')

    create(f"REPLACE INTO done_report(date_report) VALUES ('{date_report}')", user)
    await message.answer(text='✅ Записано!', reply_markup=markups.mp_menu)


@db.message_handler(commands='start')
async def start_command(message: types.Message):
    user = message.chat.id
    if selone(f"SELECT id_user FROM users WHERE id_user = '{user}'", user) is None:
        await message.answer(text=texts.start_text)
    else:
        admin_list = selone(f"SELECT id_user FROM users WHERE id_user = '{user}'", user)
        if admin_list is not None:
            await message.answer(text=texts.menu_name, reply_markup=markups.menu_admin)

@db.callback_query_handler()
async def action_callback(callback: types.CallbackQuery):
    user = callback.message.chat.id
    if 'support_' in callback.data:
        id_sup = callback.data.split('_')[1]
        if selone(f"SELECT id_work FROM wood WHERE id_sup = '{id_sup}'", user)['id_work'] == '-':
            update(f"UPDATE wood SET id_work = '{user}' WHERE id_sup = '{id_sup}'", user)
            await callback.message.edit_text(text='*Запрос принят!*\n\nОн отобразиться в меню *«💊 Личные запросы»*', parse_mode='Markdown')
        else:
            await callback.message.edit_text(text='*Запрос уже принят!*', parse_mode='Markdown')
        await callback.answer()
    elif 'supdone_' in callback.data:
        id_sup = callback.data.split('_')[1]
        update(f"UPDATE wood SET done_q = '1' WHERE id_sup = '{id_sup}'", user)
        await callback.message.edit_text(text='*Запрос завершен!*', parse_mode='Markdown')
        await callback.answer()
    elif 'obr0_' in callback.data:
        id_sup = callback.data.split('_')[1]
        update(f"UPDATE wood SET done_q = '1' WHERE id_sup = '{id_sup}'", user)
        update(f"UPDATE wood SET status_ship = 'Решил сам' WHERE id_sup = '{id_sup}'", user)

        await callback.message.edit_text(text='*Запрос завершен!*', parse_mode='Markdown')
        await callback.answer()
    elif 'obr1_' in callback.data:
        id_sup = callback.data.split('_')[1]

        update(f"UPDATE wood SET status_ship = 'Написал' WHERE id_sup = '{id_sup}'", user)
        sup = selone(f"SELECT * FROM wood WHERE id_sup = '{id_sup}'", user)
        id_user = sup["id_user"]
        name_user = selone(f"SELECT word_1 FROM wood_users WHERE id_user = '{id_user}'", user)['word_1']
        phone_user = selone(f"SELECT word_2 FROM wood_users WHERE id_user = '{id_user}'", user)['word_2']
        link_tg = selone(f"SELECT link_tg FROM wood_users WHERE id_user = '{id_user}'", user)['link_tg']

        list_det = sup['list_det'].split(' ')
        det = ' '
        if len(list_det) != 0:
            for d in list_det:
                if d == '1':
                    det += '\nНожка стула'
                elif d == '2':
                    det += '\nНожка стола'
                elif d == '3':
                    det += '\nСпинка стула'
                elif d == '4':
                    det += '\nСидение стула'
                elif d == '5':
                    det += '\nБоковая планка стула'
                elif d == '6':
                    det += '\nПеремычка стола'
                elif d == '7':
                    det += '\nСтолешница в сборе'
                elif d == '8':
                    det += '\nБоковая планка стола'
                elif d == '9':
                    det += '\nСтолешница'
                elif d == '10':
                    det += '\nФурнитура'

        mess = f'*{det}*'

        inline_key = InlineKeyboardMarkup(row_width=1)
        status_ship = 'Общение с клиентом'
        inline_key_b1 = InlineKeyboardButton(text='Зафиксировать адрес', callback_data=f'obr2_{sup["id_sup"]}')
        inline_key_b2 = InlineKeyboardButton(text='Клиент решил сам', callback_data=f'obr0_{sup["id_sup"]}')
        inline_key_b3 = InlineKeyboardButton(text='Клиент не отвечает', callback_data=f'obr5_{sup["id_sup"]}')
        inline_key.add(inline_key_b1).add(inline_key_b2).add(inline_key_b3)
        await callback.message.edit_text(f'ID запроса: *{sup["id_sup"]}*'
                             f'\nТип запроса: *{sup["word_0"]}*'
                             f'\nДата обращения: *{sup["date_q"]}*'
                             f'\n\nИмя: *{name_user}*'
                             f'\nНомер телефона: *{phone_user}*'
                             f'\nСсылка: [https://t.me/{link_tg}]'
                             f'\nТовар: *{sup["word_3"]}*'
                             f'\nГде был заказан: *{sup["word_4"]}*'
                             f'\nДата производства: *{sup["word_6"]}*'
                             f'\n\nВопрос: \n`{sup["text_q"]}`'
                             f'\n\nСтатус: *{status_ship}*', reply_markup=inline_key, parse_mode='Markdown')
        await callback.answer()
    elif 'obr2_' in callback.data:
        await callback.message.delete()
        id_sup = callback.data.split('_')[1]
        mes = 'Адрес_' + str(id_sup)
        update(f"UPDATE users SET act_wood = '{mes}' WHERE id_user = '{user}'", user)
        await callback.message.answer(text='Введите *адрес пункта выдачи* клиента:', parse_mode='Markdown', reply_markup=markups.back_mp_menu)
        await callback.answer()
    elif 'obr3_' in callback.data:
        await callback.message.delete()
        id_sup = callback.data.split('_')[1]
        mes = 'Детали_' + str(id_sup)
        update(f"UPDATE users SET act_wood = '{mes}' WHERE id_user = '{user}'", user)

        photo_id = 'AgACAgIAAxkBAAIQamXEuPjbxbp57hoRV7CZ8quvay3DAAJ91jEbrtshSsqga8N1wve9AQADAgADeQADNAQ'
        await bot.send_photo(user, photo_id, 'Введите *через пробел номера деталей*, которые нужно отправить данному клиенту \n\n_(если нужно отправить 2 одинаковые детали, то укажите номер два раза)_', reply_markup=markups.back_mp_menu)
        await callback.answer()
    elif 'obr4_' in callback.data:
        id_sup = callback.data.split('_')[1]

        update(f"UPDATE wood SET status_ship = 'Пришло' WHERE id_sup = '{id_sup}'", user)
        sup = selone(f"SELECT * FROM wood WHERE id_sup = '{id_sup}'", user)
        id_user = sup["id_user"]
        name_user = selone(f"SELECT word_1 FROM wood_users WHERE id_user = '{id_user}'", user)['word_1']
        phone_user = selone(f"SELECT word_2 FROM wood_users WHERE id_user = '{id_user}'", user)['word_2']
        link_tg = selone(f"SELECT link_tg FROM wood_users WHERE id_user = '{id_user}'", user)['link_tg']

        list_det = sup['list_det'].split(' ')
        det = ' '
        if len(list_det) != 0:
            for d in list_det:
                if d == '1':
                    det += '\nНожка стула'
                elif d == '2':
                    det += '\nНожка стола'
                elif d == '3':
                    det += '\nСпинка стула'
                elif d == '4':
                    det += '\nСидение стула'
                elif d == '5':
                    det += '\nБоковая планка стула'
                elif d == '6':
                    det += '\nПеремычка стола'
                elif d == '7':
                    det += '\nСтолешница в сборе'
                elif d == '8':
                    det += '\nБоковая планка стола'
                elif d == '9':
                    det += '\nСтолешница'
                elif d == '10':
                    det += '\nФурнитура'

        mess = f'*{det}*'

        inline_key = InlineKeyboardMarkup(row_width=1)
        status_ship = 'Пришло на пункт выдачи'
        inline_key_b1 = InlineKeyboardButton(text='Клиент не отвечает', callback_data=f'obr5_{sup["id_sup"]}')
        inline_key_b2 = InlineKeyboardButton(text='Завершить', callback_data=f'supdone_{sup["id_sup"]}')
        inline_key.add(inline_key_b1).add(inline_key_b2)
        await callback.message.edit_text(f'ID запроса: *{sup["id_sup"]}*'
                             f'\nТип запроса: *{sup["word_0"]}*'
                             f'\nДата обращения: *{sup["date_q"]}*'
                             f'\n\nИмя: *{name_user}*'
                             f'\nНомер телефона: *{phone_user}*'
                             f'\nСсылка: [https://t.me/{link_tg}]'
                             f'\nТовар: *{sup["word_3"]}*'
                             f'\nГде был заказан: *{sup["word_4"]}*'
                             f'\nДата производства: *{sup["word_6"]}*'
                             f'\n\nВопрос: \n`{sup["text_q"]}`'
                             f'\n\nАдрес пункта: `{sup["adress_client"]}`'
                             f'\n\nДетали: *{mess}*'
                             f'\n\nСтатус: *{status_ship}*', reply_markup=inline_key, parse_mode='Markdown')
        await callback.answer()
    elif 'obr5_' in callback.data:
        id_sup = callback.data.split('_')[1]
        update(f"UPDATE wood SET done_q = '1' WHERE id_sup = '{id_sup}'", user)
        update(f"UPDATE wood SET status_ship = 'Нет ответа' WHERE id_sup = '{id_sup}'", user)

        await callback.message.edit_text(text='*Запрос закрыт!*', parse_mode='Markdown')
        await callback.answer()
    elif 'ship_' in callback.data:
        await callback.message.delete()
        id_sup = callback.data.split('_')[1]
        mes = 'Заказа_' + id_sup
        update(f"UPDATE users SET act_wood = '{mes}' WHERE id_user = '{user}'", user)
        await callback.message.answer(text='Пришлите *QR заказа* документом .pdf', parse_mode='Markdown', reply_markup=markups.back_mp_menu)
        await callback.answer()
    elif 'stat_' in callback.data:
        month = callback.data.split('_')[1]
        month_test = month + ' 1'
        stat_list_test = selist(f"SELECT * FROM skaz_stat WHERE month = '{month_test}'", user)
        stat_list = selist(f"SELECT * FROM skaz_stat", user)
        if len(stat_list_test) != 0:
            for stat in stat_list:
                if month in stat['month']:
                    name_team = stat["name_team"]
                    if name_team == 'Общая статистика':
                        aver = round((int(stat["count_day"]) + int(stat["wood"])) / 30, 2)
                        await callback.message.answer(text=f'*{name_team}*\n\n'
                                                           f'📆 Месяц: *{month}*\n'
                                                           f'—————————————————————\n'
                                                           f'🔨 Сделано изделий: *{stat["wood"]}*\n'
                                                           f'🌙 Ночные: *{stat["count_day"]}*\n'
                                                           f'💣 Возвраты: *{stat["voz"]}*\n'
                                                           f'🚛 Разгрузки: *{stat["raz"]}*\n'
                                                           f'—————————————————————\n'
                                                           f'📦 Всего изготовлено *{int(stat["count_day"]) + int(stat["wood"])}*\n'
                                                           f'⚒ Среднее за сутки: *{aver}*\n\n')
                    else:
                        if int(stat["count_day"]) == 0:
                            aver = 0
                        else:
                            aver = round(int(stat["wood"]) / int(stat["count_day"]), 2)
                        list_users = selist(f"SELECT name_user FROM skaz_users WHERE team_user = '{name_team}'", user)
                        mes_users = []
                        for u in list_users:
                            mes_users.append(u['name_user'])

                        await callback.message.answer(text=f'📆 Месяц: *{month}*\n'
                                                          f'🎒 Команда: *{name_team}*\n'
                                                          f'_{", ".join(mes_users)}_\n'
                                                          f'—————————————————————\n'
                                                          f'🔨 Сделано изделий: *{stat["wood"]}*\n'
                                                          f'⚒ Среднее за смену: *{aver}*\n\n'
                                                          f'💣 Возвраты: *{stat["voz"]}*\n'
                                                          f'🚛 Разгрузки: *{stat["raz"]}*\n'
                                                          f'—————————————————————\n'
                                                          f'💰 Количество смен: *{stat["count_day"]}*')

        else:
            await callback.message.answer('Статистика пуста!')

        await callback.answer()
    elif 'instr_' in callback.data:
        type_instr = callback.data.split('_')[1]
        if type_instr == 'pp':
            await bot.send_document(user, 'BQACAgIAAxkBAAIGAAFltzmBagYZ5A5KUHhbaHpEJfWLywACTj8AAjTLwEnn-i3-8cAXtzQE', protect_content=True)
        await callback.answer()
    elif 'sync_' in callback.data:
        type_sync = callback.data.split('_')[1]
        if type_sync == 'poz':
            await callback.message.edit_text(text='Синхронизация...\n🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥')
            worksheet = sh.worksheet('Заказы маркетплейс 2024')
            await callback.message.edit_text(text='Синхронизация...\n🟩🟥🟥🟥🟥🟥🟥🟥🟥🟥')
            list_value = set(worksheet.row_values(1))
            list_items = []
            await callback.message.edit_text(text='Синхронизация...\n🟩🟩🟥🟥🟥🟥🟥🟥🟥🟥')
            for val in list_value:
                if len(val) == 0 or val == 'Сумма WB ООО' or val == 'Сумма OZON ООО' or val == 'Сумма ЯМ ООО' \
                        or val == 'Сумма ММ ООО' or val == 'Сумма KE ООО' or val == 'Сумма ДМ ООО' \
                        or val == 'Сумма Авито ООО' or val == 'Сумма Instagram ООО' or val == 'Сумма WB ИП' \
                        or val == 'Сумма OZON ИП' or val == 'Сумма ЯМ ИП' or val == 'Сумма ММ ИП' \
                        or val == '-' or val == 'Сумма KE ИП' or val == 'Сумма ДМ ИП' or val == 'Сумма Авито ИП' or val == 'Сумма Instagram ИП' \
                        or val == 'Заказы 1 товар' or val == 'Заказы 2 товар' or val == 'Заказы 3 товар' or val == 'Заказы 4 товар' or val == 'Заказы 5 товар' \
                        or val == 'Заказы 6 товар' or val == 'Общая сумма':
                    pass
                else:
                    list_items.append(val)
            await callback.message.edit_text(text='Синхронизация...\n🟩🟩🟩🟥🟥🟥🟥🟥🟥🟥')

            list_value = set(worksheet.row_values(2))
            list_mp = []
            await callback.message.edit_text(text='Синхронизация...\n🟩🟩🟩🟩🟩🟥🟥🟥🟥🟥')
            for val in list_value:
                if len(val) == 0 or val == '-':
                    pass
                else:
                    list_mp.append(val)
            await callback.message.edit_text(text='Синхронизация...\n🟩🟩🟩🟩🟩🟩🟥🟥🟥🟥')

            list_value = set(worksheet.row_values(3))
            list_ul = []
            await callback.message.edit_text(text='Синхронизация...\n🟩🟩🟩🟩🟩🟩🟩🟩🟥🟥')
            for val in list_value:
                if len(val) == 0 or val == '-':
                    pass
                else:
                    list_ul.append(val)
            await callback.message.edit_text(text='Синхронизация...\n🟩🟩🟩🟩🟩🟩🟩🟩🟩🟥')

            for i in list_items:
                for j in list_ul:
                    for k in list_mp:
                        name_item = i + '_' + j + '_' + k
                        create(f"INSERT INTO price_wood(name_item, price_item) VALUES ('{name_item}', 0)", user)

            await callback.message.edit_text(text='✅ Синхронизация успешна!')
        await callback.answer()
    elif 'name_' in callback.data:
        name_item = callback.data.split('_')[1]
        update(f"UPDATE users SET act_wood = '{name_item}' WHERE id_user = '{user}'", user)
        list_values = selist(f"SELECT * FROM price_wood", user)
        inline_key = InlineKeyboardMarkup(row_width=1)

        list_ul_old = []

        for i in list_values:
            name_item = i['name_item'].split('_')
            item_ul = name_item[1]
            list_ul_old.append(item_ul)

        list_ul = set(list_ul_old)

        for v in list_ul:
            inline_key_b1 = InlineKeyboardButton(text=f'{v}', callback_data=f'ul_{v}')
            inline_key.add(inline_key_b1)

        await callback.message.edit_text(text='🎩 Выберите ЮЛ:', reply_markup=inline_key)
        await callback.answer()
    elif 'ul_' in callback.data:
        name_item = callback.data.split('_')[1]
        all_name = selone(f"SELECT act_wood FROM users WHERE id_user = '{user}'", user)['act_wood'] + '_' + name_item
        update(f"UPDATE users SET act_wood = '{all_name}' WHERE id_user = '{user}'", user)
        list_values = selist(f"SELECT * FROM price_wood", user)
        inline_key = InlineKeyboardMarkup(row_width=1)

        list_mp_old = []

        for i in list_values:
            name_item = i['name_item'].split('_')
            item_mp = name_item[2]
            list_mp_old.append(item_mp)

        list_mp = set(list_mp_old)

        for v in list_mp:
            inline_key_b1 = InlineKeyboardButton(text=f'{v}', callback_data=f'price_{v}')
            inline_key.add(inline_key_b1)

        await callback.message.edit_text(text='🛒 Выберите Маркетплейс:', reply_markup=inline_key)
        await callback.answer()
    elif 'price_' in callback.data:
        name_item = callback.data.split('_')[1]
        all_name = selone(f"SELECT act_wood FROM users WHERE id_user = '{user}'", user)['act_wood'] + '_' + name_item

        id_item = selone(f"SELECT id_item FROM price_wood WHERE name_item = '{all_name}'", user)['id_item']
        price_item = selone(f"SELECT price_item FROM price_wood WHERE id_item = '{id_item}'", user)['price_item']
        val = f'Цена_{id_item}'
        update(f"UPDATE users SET act_wood = '{val}' WHERE id_user = '{user}'", user)
        await callback.message.edit_text(text=f'—————————————————————', parse_mode='HTML')
        await callback.message.answer(text=f'Позиция: <b>{all_name}</b>\nСтоимость: <b>{price_item} р.</b>', parse_mode='HTML')
        await callback.message.answer(text=f'💵 Введите стоимость цифрами:', parse_mode='HTML')
        await callback.answer()
    elif 'cancel_' in callback.data:
        await callback.message.delete()
        id_ship = callback.data.split('_')[1]

        inline_m = InlineKeyboardMarkup(row_width=2)
        inline_m_b1 = InlineKeyboardButton(text='Да', callback_data=f'yescenc_{id_ship}')
        inline_m_b2 = InlineKeyboardButton(text='Нет', callback_data=f'noscenc_{id_ship}')
        inline_m.add(inline_m_b1).add(inline_m_b2)

        await callback.message.answer(text=f'Вы уверены, что хотите отменить заявку?', reply_markup=inline_m)
        await callback.answer()
    elif 'yescenc_' in callback.data:
        await callback.message.delete()
        id_ship = callback.data.split('_')[1]
        list_ship = selist(f"SELECT * FROM shipping WHERE id_ship = '{id_ship}'", user)[0]

        list_all_users = selist(f"SELECT * FROM users WHERE company = 'Босс'", user)
        list_users = []
        for us in list_all_users:
            if 'log' in us['notif']:
                list_users.append(us)
        for user1 in list_users:
            try:
                chat_id = str(user1["id_user"])
                destination_bot = Bot(token='6682205213:AAFFV1avM8cVCZhgv-K8pzKeJ_c20Wle_P4')
                await destination_bot.send_message(chat_id, f'Заявка с ID: {id_ship} отменена.\n\n'
                                                            f'Тип: *{list_ship["type_ship"]}*\n'
                                                            f'Предмет: *{list_ship["item_ship"]}*\n'
                                                            f'Адрес загрузки: *{list_ship["adress_begin"]}*\n'
                                                            f'Адрес разгрузки: *{list_ship["adress_end"]}*\n', parse_mode='Markdown')
            except Exception as e:
                pass

        update(f"UPDATE shipping SET status_ship = 'Отменен' WHERE id_ship = '{id_ship}'", user)
        await callback.message.answer(text='Статус «Отменен» проставлен!')
        await callback.answer()
    elif 'noscenc_' in callback.data:
        await callback.message.delete()
        await callback.answer()

@db.message_handler()
async def send_text(message: types.Message):
    user = message.chat.id

    if user == -1002146643966:
        pass

    elif selone(f"SELECT id_user FROM users WHERE id_user = '{user}'", user) is None:
        await message.answer(text=texts.start_text)

    else:
        if '*' in message.text or '_' in message.text:
            await message.answer(text='Сообщения не должно содержать * или _')

        else:
            # Главное меню
            if message.text == markups.menu_main:
                defaul_values(user)
                await message.answer(text=texts.menu_name, reply_markup=markups.menu_admin)

            # ЦЕХ меню
            elif message.text == markups.menu_admin_b2 or message.text == markups.back_tseh_b:
                if selone(f"SELECT company FROM users WHERE id_user = '{user}'", user)['company'] == 'Мастер' or selone(f"SELECT company FROM users WHERE id_user = '{user}'", user)['company'] == 'Сборщик' or selone(f"SELECT company FROM users WHERE id_user = '{user}'", user)['company'] == 'Босс':
                    defaul_values(user)
                    await message.answer(text=texts.menu_tseh, reply_markup=markups.tseh_menu)
                else:
                    await message.answer(text='У вас нет доступа!')

            # Табель
            elif message.text == markups.tseh_menu_b1:
                delta_1 = datetime.timedelta(hours=5)
                now = datetime.datetime.now()
                if int(now.day) < 10:
                    day_edit = '0' + str(now.day)
                else:
                    day_edit = now.day

                if int(now.month) < 10:
                    month_edit = '0' + str(now.month)
                else:
                    month_edit = now.month

                if now.month == 1:
                    name_list = f"Январь {now.year}"
                elif now.month == 2:
                    name_list = f"Февраль {now.year}"
                elif now.month == 3:
                    name_list = f"Март {now.year}"
                elif now.month == 4:
                    name_list = f"Апрель {now.year}"
                elif now.month == 5:
                    name_list = f"Май {now.year}"
                elif now.month == 6:
                    name_list = f"Июнь {now.year}"
                elif now.month == 7:
                    name_list = f"Июль {now.year}"
                elif now.month == 8:
                    name_list = f"Август {now.year}"
                elif now.month == 9:
                    name_list = f"Сентябрь {now.year}"
                elif now.month == 10:
                    name_list = f"Октябрь {now.year}"
                elif now.month == 11:
                    name_list = f"Ноябрь {now.year}"
                elif now.month == 12:
                    name_list = f"Декабрь {now.year}"



                list_tab_old = selist(f"SELECT * FROM skaz_users WHERE id_user = '{user}'", user)
                if len(list_tab_old) != 0:
                    list_tab = list_tab_old[0]
                    await message.answer(text=f'ℹ️ Табель сотрудника с номером: *{list_tab["id_user"]}*\n\n'
                                              f'📅 Месяц: *{name_list}*\n'
                                              f'🏷 Имя: *{list_tab["name_user"]}*\n'
                                              f'🎒 Команда: *{list_tab["team_user"]}*\n\n'
                                              f'—————————————————————\n\n'
                                              f'🔨 Отработано:\n'
                                              f'Часов: *{list_tab["hour_user"]}*\n'
                                              f'Сумма по часам: *{list_tab["sum_hour_user"]}*\n\n'
                                              f'🏆 Доп. мотивация:\n'
                                              f'Изделий дополнительно: *{list_tab["dop_user"]}*\n'
                                              f'Сумма: *{list_tab["sum_dop_user"]}*\n\n'
                                              f'💣 Возвраты:\n'
                                              f'Переупаковано: *{list_tab["voz_user"]}*\n'
                                              f'Сумма: *{list_tab["sum_voz_user"]}*\n\n'
                                              f'🌒 Ночные смены:\n'
                                              f'Сумма: *{list_tab["night_user"]}*\n\n'
                                              f'🚛 Разгрузки:\n'
                                              f'Разгружено: *{list_tab["raz_user"]}*\n'
                                              f'Сумма: *{list_tab["sum_raz_user"]}*\n\n'
                                              f'🤑 Премия:\n'
                                              f'Сумма: *{list_tab["prem"]}*\n\n'
                                              f'—————————————————————\n\n'
                                              f'🌴 Дней отпуска: *{list_tab["otp"]}*\n'
                                              f'💶 Сумма за отпуск: *{list_tab["otp_sum"]}*\n\n'
                                              f'—————————————————————\n\n'
                                              f'💰 Общая заработная плата: *{list_tab["main_user"]}*\n\n'
                                              f'💸 Выплачено: *{list_tab["pay_user"]}*\n'
                                              f'⛔️ Штраф: *{list_tab["shtraf"]}*\n\n'
                                              f'—————————————————————\n\n'
                                              f'💵 Остаток: *{list_tab["need_user"]}*\n')
                elif selone(f"SELECT company FROM users WHERE id_user = '{user}'", user)['company'] == 'Босс':
                    delta_1 = datetime.timedelta(hours=5)
                    now = datetime.datetime.now()
                    now_day = str(now.day)
                    now_month = int(now.month) - 1

                    if now_month == 1:
                        name_list = f"Январь {now.year}"
                    elif now_month == 2:
                        name_list = f"Февраль {now.year}"
                    elif now_month == 3:
                        name_list = f"Март {now.year}"
                    elif now_month == 4:
                        name_list = f"Апрель {now.year}"
                    elif now_month == 5:
                        name_list = f"Май {now.year}"
                    elif now_month == 6:
                        name_list = f"Июнь {now.year}"
                    elif now_month == 7:
                        name_list = f"Июль {now.year}"
                    elif now_month == 8:
                        name_list = f"Август {now.year}"
                    elif now_month == 9:
                        name_list = f"Сентябрь {now.year}"
                    elif now_month == 10:
                        name_list = f"Октябрь {now.year}"
                    elif now_month == 11:
                        name_list = f"Ноябрь {now.year}"
                    elif now_month == 12:
                        name_list = f"Декабрь {now.year}"

                    list_tab_old = selist(f"SELECT * FROM skaz_users", user)
                    for list_tab in list_tab_old:
                        mess = f'ℹ️ Табель сотрудника с номером: *{list_tab["id_user"]}*\n\n' \
                               f'📅 Месяц: *{name_list}*\n' \
                               f'🏷 Имя: *{list_tab["name_user"]}*\n' \
                               f'🎒 Команда: *{list_tab["team_user"]}*\n\n' \
                               f'—————————————————————\n\n' \
                               f'🔨 Отработано:\n' \
                               f'Часов: *{list_tab["hour_user"]}*\n' \
                               f'Сумма по часам: *{list_tab["sum_hour_user"]}*\n\n' \
                               f'🏆 Доп. мотивация:\n' \
                               f'Изделий дополнительно: *{list_tab["dop_user"]}*\n' \
                               f'Сумма: *{list_tab["sum_dop_user"]}*\n\n' \
                               f'💣 Возвраты:\n' \
                               f'Переупаковано: *{list_tab["voz_user"]}*\n' \
                               f'Сумма: *{list_tab["sum_voz_user"]}*\n\n' \
                               f'🌒 Ночные смены:\n' \
                               f'Сумма: *{list_tab["night_user"]}*\n\n' \
                               f'🚛 Разгрузки:\n' \
                               f'Разгружено: *{list_tab["raz_user"]}*\n' \
                               f'Сумма: *{list_tab["sum_raz_user"]}*\n\n' \
                               f'🤑 Премия:\n' \
                               f'Сумма: *{list_tab["prem"]}*\n\n' \
                               f'—————————————————————\n\n' \
                               f'🌴 Дней отпуска: *{list_tab["otp"]}*\n' \
                               f'💶 Сумма за отпуск: *{list_tab["otp_sum"]}*\n\n' \
                               f'—————————————————————\n\n' \
                               f'💰 Общая заработная плата: *{list_tab["main_user"]}*\n\n' \
                               f'💸 Выплачено: *{list_tab["pay_user"]}*\n' \
                               f'⛔️ Штраф: *{list_tab["shtraf"]}*\n\n' \
                               f'—————————————————————\n\n' \
                               f'💵 Нужно выплатить: *{list_tab["need_user"]}*\n'

                        await message.answer(mess, parse_mode='Markdown')

                else:
                    await message.answer(text='Табель не может быть сформирован для Вас.')

            # Статистика
            elif message.text == markups.tseh_menu_b2:
                inline_key = InlineKeyboardMarkup(row_width=3)
                inline_key_b1 = InlineKeyboardButton(text='Январь', callback_data=f'stat_Январь')
                inline_key_b2 = InlineKeyboardButton(text='Февраль', callback_data=f'stat_Февраль')
                inline_key_b3 = InlineKeyboardButton(text='Март', callback_data=f'stat_Март')
                inline_key_b4 = InlineKeyboardButton(text='Апрель', callback_data=f'stat_Апрель')
                inline_key_b5 = InlineKeyboardButton(text='Май', callback_data=f'stat_Май')
                inline_key_b6 = InlineKeyboardButton(text='Июнь', callback_data=f'stat_Июнь')
                inline_key_b7 = InlineKeyboardButton(text='Июль', callback_data=f'stat_Июль')
                inline_key_b8 = InlineKeyboardButton(text='Август', callback_data=f'stat_Август')
                inline_key_b9 = InlineKeyboardButton(text='Сентябрь', callback_data=f'stat_Сентябрь')
                inline_key_b10 = InlineKeyboardButton(text='Октябрь', callback_data=f'stat_Октябрь')
                inline_key_b11 = InlineKeyboardButton(text='Ноябрь', callback_data=f'stat_Ноябрь')
                inline_key_b12 = InlineKeyboardButton(text='Декабрь', callback_data=f'stat_Декабрь')
                inline_key.add(inline_key_b1, inline_key_b2, inline_key_b3).add(inline_key_b4, inline_key_b5, inline_key_b6).add(inline_key_b7, inline_key_b8, inline_key_b9).add(inline_key_b10, inline_key_b11, inline_key_b12)
                await message.answer(text='📆')
                await message.answer(text='Выберите месяц:', reply_markup=inline_key)

            # Предложить
            elif message.text == markups.tseh_menu_b3:
                update(f"UPDATE users SET act_wood = 'Предложить' WHERE id_user = '{user}'", user)
                await message.answer(text='Данный функционал предназначен для того, чтобы *предложить идеи* ⭐️ по улучшению работы.\n\nАвторы полезных и развернутых идей будут вознаграждены *премией* 💰.', reply_markup=markups.back_tseh_menu)
                await message.answer(text='Опишите свою идею:')
            elif selone(f"SELECT act_wood FROM users WHERE id_user = '{user}'", user)['act_wood'] == 'Предложить':
                update(f"UPDATE users SET act_wood = ' ' WHERE id_user = '{user}'", user)
                name_user = selone(f"SELECT name_user FROM users WHERE id_user = '{user}'", user)['name_user']
                mes = f'*💡 Идея от сотрудника:*\n\n' \
                      f'Имя: *{name_user}*\n\n' \
                      f'_{message.text}_'
                await bot.send_message(chat_id=-1002146643966, text=mes, message_thread_id=6, parse_mode='Markdown')
                await message.answer(text='Отлично! *Предложение будет рассмотрено*.', reply_markup=markups.tseh_menu)

            # Вакансии
            elif message.text == markups.tseh_menu_b4:
                await message.answer(text='Вакансий нет')

            # Инструкции
            elif message.text == markups.tseh_menu_b5:
                inline_key = InlineKeyboardMarkup(row_width=1)
                inline_key_b1 = InlineKeyboardButton(text='🏥 Первая помощь', callback_data='instr_pp')
                inline_key.add(inline_key_b1)
                await message.answer(text='Выберите инструкцию:', reply_markup=inline_key)

            # Менеджмент МП меню
            elif message.text == markups.menu_admin_b1 or message.text == markups.back_mp_b:
                if selone(f"SELECT company FROM users WHERE id_user = '{user}'", user)['company'] == 'Менеджер МП' or selone(f"SELECT company FROM users WHERE id_user = '{user}'", user)['company'] == 'Босс':
                    defaul_values(user)
                    await message.answer(text=texts.menu_mp, reply_markup=markups.mp_menu)
                else:
                    await message.answer(text='У вас нет доступа!')

            # Остаток на складе
            elif message.text == markups.mp_menu_b3:
                name_list = "Складской учет"

                worksheet = sh.worksheet(name_list)

                list_g = worksheet.row_values(4)

                await bot.send_message(chat_id=user, text=f'Остаток на ФФ:\nРастущий 1: *{list_g[5]}*\nРастущий 2: *{list_g[6]}*', parse_mode='Markdown')

            # Отзыв
            elif message.text == markups.mp_menu_b9:
                update(f"UPDATE users SET act_wood = 'otz' WHERE id_user = '{user}'", user)
                await message.answer("Отправьте фото отзыва, которое будет разослано сотрудникам цеха:")
                await message.answer(text="Для возврата нажмите 'Отмена'", reply_markup=markups.back_mp_menu)

            # Непринятые запросы
            elif message.text == markups.mp_menu_b1:
                sup_list = selist(f"SELECT * FROM wood WHERE id_work = '-' AND word_0 <> '' AND done_q = 0 AND date_q <> ''", user)

                if len(sup_list) > 0:
                    for sup in sup_list:
                        id_user = sup["id_user"]
                        name_user = selone(f"SELECT word_1 FROM wood_users WHERE id_user = '{id_user}'", user)['word_1']
                        phone_user = selone(f"SELECT word_2 FROM wood_users WHERE id_user = '{id_user}'", user)['word_2']
                        link_tg = selone(f"SELECT link_tg FROM wood_users WHERE id_user = '{id_user}'", user)['link_tg']
                        inline_key = InlineKeyboardMarkup(row_width=1)
                        inline_key_b1 = InlineKeyboardButton(text='Принять',
                                                             callback_data=f'support_{sup["id_sup"]}')
                        inline_key.add(inline_key_b1)
                        await message.answer(f'ID запроса: <b>{sup["id_sup"]}</b>'
                                             f'\nТип запроса: <b>{sup["word_0"]}</b>'
                                             f'\nДата обращения: <b>{sup["date_q"]}</b>'
                                             f'\n\nИмя: <b>{name_user}</b>'
                                             f'\nНомер телефона: <b>{phone_user}</b>'
                                             f'\nСсылка: <b>https://t.me/{link_tg}</b>'
                                             f'\nТовар: <b>{sup["word_3"]}</b>'
                                             f'\nГде был заказан: <b>{sup["word_4"]}</b>'
                                             f'\nДата производства: <b>{sup["word_6"]}</b>'
                                             f'\n\nВопрос: \n<b>{sup["text_q"]}</b>', reply_markup=inline_key, parse_mode='HTML')
                else:
                    await message.answer('Запросов нет!')

            # Личные запросы
            elif message.text == markups.mp_menu_b2:
                sup_list = selist(f"SELECT * FROM wood WHERE id_work = '{user}' AND done_q = 0", user)

                if len(sup_list) > 0:
                    for sup in sup_list:
                        id_user = sup["id_user"]
                        name_user = selone(f"SELECT word_1 FROM wood_users WHERE id_user = '{id_user}'", user)['word_1']
                        phone_user = selone(f"SELECT word_2 FROM wood_users WHERE id_user = '{id_user}'", user)['word_2']
                        link_tg = selone(f"SELECT link_tg FROM wood_users WHERE id_user = '{id_user}'", user)['link_tg']

                        list_det = sup['list_det'].split(' ')
                        det = ' '
                        if len(list_det) != 0:
                            for d in list_det:
                                if d == '1':
                                    det += '\nНожка стула'
                                elif d == '2':
                                    det += '\nНожка стола'
                                elif d == '3':
                                    det += '\nСпинка стула'
                                elif d == '4':
                                    det += '\nСидение стула'
                                elif d == '5':
                                    det += '\nБоковая планка стула'
                                elif d == '6':
                                    det += '\nПеремычка стола'
                                elif d == '7':
                                    det += '\nСтолешница в сборе'
                                elif d == '8':
                                    det += '\nБоковая планка стола'
                                elif d == '9':
                                    det += '\nСтолешница'
                                elif d == '10':
                                    det += '\nФурнитура'

                        mess = f'*{det}*'

                        inline_key = InlineKeyboardMarkup(row_width=1)
                        status_ship = 'Не обработан'
                        if sup["status_ship"] == 'Не обработан':
                            status_ship = 'Не списались'
                            inline_key_b1 = InlineKeyboardButton(text='Написал клиенту', callback_data=f'obr1_{sup["id_sup"]}')
                            inline_key.add(inline_key_b1)
                            await message.answer(f'ID запроса: *{sup["id_sup"]}*'
                                                 f'\nТип запроса: *{sup["word_0"]}*'
                                                 f'\nДата обращения: *{sup["date_q"]}*'
                                                 f'\n\nИмя: *{name_user}*'
                                                 f'\nНомер телефона: *{phone_user}*'
                                                 f'\nСсылка: [https://t.me/{link_tg}]'
                                                 f'\nТовар: *{sup["word_3"]}*'
                                                 f'\nГде был заказан: *{sup["word_4"]}*'
                                                 f'\nДата производства: *{sup["word_6"]}*'
                                                 f'\n\nВопрос: \n`{sup["text_q"]}`'
                                                 f'\n\nСтатус: *{status_ship}*', reply_markup=inline_key, parse_mode='Markdown')
                        elif sup["status_ship"] == 'Написал':
                            status_ship = 'Общение с клиентом'
                            inline_key_b1 = InlineKeyboardButton(text='Зафиксировать адрес', callback_data=f'obr2_{sup["id_sup"]}')
                            inline_key_b2 = InlineKeyboardButton(text='Клиент решил сам', callback_data=f'obr0_{sup["id_sup"]}')
                            inline_key_b3 = InlineKeyboardButton(text='Клиент не отвечает', callback_data=f'obr5_{sup["id_sup"]}')
                            inline_key.add(inline_key_b1).add(inline_key_b2).add(inline_key_b3)
                            await message.answer(f'ID запроса: *{sup["id_sup"]}*'
                                                 f'\nТип запроса: *{sup["word_0"]}*'
                                                 f'\nДата обращения: *{sup["date_q"]}*'
                                                 f'\n\nИмя: *{name_user}*'
                                                 f'\nНомер телефона: *{phone_user}*'
                                                 f'\nСсылка: [https://t.me/{link_tg}]'
                                                 f'\nТовар: *{sup["word_3"]}*'
                                                 f'\nГде был заказан: *{sup["word_4"]}*'
                                                 f'\nДата производства: *{sup["word_6"]}*'
                                                 f'\n\nВопрос: \n`{sup["text_q"]}`'
                                                 f'\n\nСтатус: *{status_ship}*', reply_markup=inline_key, parse_mode='Markdown')
                        elif sup["status_ship"] == 'Адрес':
                            status_ship = 'Общение с клиентом'
                            inline_key_b1 = InlineKeyboardButton(text='Зафиксировать детали', callback_data=f'obr3_{sup["id_sup"]}')
                            inline_key_b2 = InlineKeyboardButton(text='Клиент решил сам', callback_data=f'obr0_{sup["id_sup"]}')
                            inline_key.add(inline_key_b1).add(inline_key_b2)
                            await message.answer(f'ID запроса: *{sup["id_sup"]}*'
                                                 f'\nТип запроса: *{sup["word_0"]}*'
                                                 f'\nДата обращения: *{sup["date_q"]}*'
                                                 f'\n\nИмя: *{name_user}*'
                                                 f'\nНомер телефона: *{phone_user}*'
                                                 f'\nСсылка: [https://t.me/{link_tg}]'
                                                 f'\nТовар: *{sup["word_3"]}*'
                                                 f'\nГде был заказан: *{sup["word_4"]}*'
                                                 f'\nДата производства: *{sup["word_6"]}*'
                                                 f'\n\nВопрос: \n`{sup["text_q"]}`'
                                                 f'\n\nАдрес пункта: `{sup["adress_client"]}`'
                                                 f'\n\nСтатус: *{status_ship}*', reply_markup=inline_key, parse_mode='Markdown')
                        elif sup["status_ship"] == 'Детали':
                            status_ship = 'Общение с клиентом'
                            inline_key_b1 = InlineKeyboardButton(text='Передать в цех', callback_data=f'ship_{sup["id_sup"]}')
                            inline_key_b2 = InlineKeyboardButton(text='Клиент решил сам', callback_data=f'obr0_{sup["id_sup"]}')
                            inline_key.add(inline_key_b1).add(inline_key_b2)
                            await message.answer(f'ID запроса: *{sup["id_sup"]}*'
                                                 f'\nТип запроса: *{sup["word_0"]}*'
                                                 f'\nДата обращения: *{sup["date_q"]}*'
                                                 f'\n\nИмя: *{name_user}*'
                                                 f'\nНомер телефона: *{phone_user}*'
                                                 f'\nСсылка: [https://t.me/{link_tg}]'
                                                 f'\nТовар: *{sup["word_3"]}*'
                                                 f'\nГде был заказан: *{sup["word_4"]}*'
                                                 f'\nДата производства: *{sup["word_6"]}*'
                                                 f'\n\nВопрос: \n`{sup["text_q"]}`'
                                                 f'\n\nАдрес пункта: `{sup["adress_client"]}`'
                                                 f'\n\nДетали: *{mess}*'
                                                 f'\n\nСтатус: *{status_ship}*', reply_markup=inline_key, parse_mode='Markdown')
                        elif sup["status_ship"] == 'Обрабатывается в цеху':
                            status_ship = 'Обрабатывается в цеху'
                            await message.answer(f'ID запроса: *{sup["id_sup"]}*'
                                                 f'\nТип запроса: *{sup["word_0"]}*'
                                                 f'\nДата обращения: *{sup["date_q"]}*'
                                                 f'\n\nИмя: *{name_user}*'
                                                 f'\nНомер телефона: *{phone_user}*'
                                                 f'\nСсылка: [https://t.me/{link_tg}]'
                                                 f'\nТовар: *{sup["word_3"]}*'
                                                 f'\nГде был заказан: *{sup["word_4"]}*'
                                                 f'\nДата производства: *{sup["word_6"]}*'
                                                 f'\n\nВопрос: \n`{sup["text_q"]}`'
                                                 f'\n\nАдрес пункта: `{sup["adress_client"]}`'
                                                 f'\n\nДетали: *{mess}*'
                                                 f'\n\nСтатус: *{status_ship}*', parse_mode='Markdown')
                        elif sup["status_ship"] == 'Обработано, ждет отправки':
                            status_ship = 'Обработано, ждет отправки'
                            await message.answer(f'ID запроса: *{sup["id_sup"]}*'
                                                 f'\nТип запроса: *{sup["word_0"]}*'
                                                 f'\nДата обращения: *{sup["date_q"]}*'
                                                 f'\n\nИмя: *{name_user}*'
                                                 f'\nНомер телефона: *{phone_user}*'
                                                 f'\nСсылка: [https://t.me/{link_tg}]'
                                                 f'\nТовар: *{sup["word_3"]}*'
                                                 f'\nГде был заказан: *{sup["word_4"]}*'
                                                 f'\nДата производства: *{sup["word_6"]}*'
                                                 f'\n\nВопрос: \n`{sup["text_q"]}`'
                                                 f'\n\nАдрес пункта: `{sup["adress_client"]}`'
                                                 f'\n\nДетали: *{mess}*'
                                                 f'\n\nСтатус: *{status_ship}*', parse_mode='Markdown')
                        elif sup["status_ship"] == 'Отправлено':
                            status_ship = 'Отправлено клиенту'
                            inline_key_b1 = InlineKeyboardButton(text='Пришло на пункт выдачи', callback_data=f'obr4_{sup["id_sup"]}')
                            inline_key.add(inline_key_b1)
                            await message.answer(f'ID запроса: *{sup["id_sup"]}*'
                                                 f'\nТип запроса: *{sup["word_0"]}*'
                                                 f'\nДата обращения: *{sup["date_q"]}*'
                                                 f'\n\nИмя: *{name_user}*'
                                                 f'\nНомер телефона: *{phone_user}*'
                                                 f'\nСсылка: [https://t.me/{link_tg}]'
                                                 f'\nТовар: *{sup["word_3"]}*'
                                                 f'\nГде был заказан: *{sup["word_4"]}*'
                                                 f'\nДата производства: *{sup["word_6"]}*'
                                                 f'\n\nВопрос: \n`{sup["text_q"]}`'
                                                 f'\n\nАдрес пункта: `{sup["adress_client"]}`'
                                                 f'\n\nДетали: *{mess}*'
                                                 f'\n\nСтатус: *{status_ship}*', reply_markup=inline_key, parse_mode='Markdown')
                        elif sup["status_ship"] == 'Пришло':
                            status_ship = 'Пришло на пункт выдачи'
                            inline_key_b1 = InlineKeyboardButton(text='Клиент не отвечает', callback_data=f'obr5_{sup["id_sup"]}')
                            inline_key_b2 = InlineKeyboardButton(text='Завершить', callback_data=f'supdone_{sup["id_sup"]}')
                            inline_key.add(inline_key_b1).add(inline_key_b2)
                            await message.answer(f'ID запроса: *{sup["id_sup"]}*'
                                                 f'\nТип запроса: *{sup["word_0"]}*'
                                                 f'\nДата обращения: *{sup["date_q"]}*'
                                                 f'\n\nИмя: *{name_user}*'
                                                 f'\nНомер телефона: *{phone_user}*'
                                                 f'\nСсылка: [https://t.me/{link_tg}]'
                                                 f'\nТовар: *{sup["word_3"]}*'
                                                 f'\nГде был заказан: *{sup["word_4"]}*'
                                                 f'\nДата производства: *{sup["word_6"]}*'
                                                 f'\n\nВопрос: \n`{sup["text_q"]}`'
                                                 f'\n\nАдрес пункта: `{sup["adress_client"]}`'
                                                 f'\n\nДетали: *{mess}*'
                                                 f'\n\nСтатус: *{status_ship}*', reply_markup=inline_key, parse_mode='Markdown')
                        elif sup["status_ship"] == 'Решил сам':
                            status_ship = 'Клиент решил сам'
                        elif sup["status_ship"] == 'Нет ответа':
                            status_ship = 'Нет ответа от клиента'


                else:
                    await message.answer('Личный запросов нет!')
            elif 'Адрес_' in selone(f"SELECT act_wood FROM users WHERE id_user = '{user}'", user)['act_wood']:
                id_sup = selone(f"SELECT act_wood FROM users WHERE id_user = '{user}'", user)['act_wood'].split("_")[1]
                update(f"UPDATE users SET act_wood = '' WHERE id_user = '{user}'", user)
                update(f"UPDATE wood SET adress_client = '{message.text}' WHERE id_sup = '{id_sup}'", user)
                update(f"UPDATE wood SET status_ship = 'Адрес' WHERE id_sup = '{id_sup}'", user)
                sup = selone(f"SELECT * FROM wood WHERE id_sup = '{id_sup}'", user)
                id_user = sup["id_user"]
                name_user = selone(f"SELECT word_1 FROM wood_users WHERE id_user = '{id_user}'", user)['word_1']
                phone_user = selone(f"SELECT word_2 FROM wood_users WHERE id_user = '{id_user}'", user)['word_2']
                link_tg = selone(f"SELECT link_tg FROM wood_users WHERE id_user = '{id_user}'", user)['link_tg']

                list_det = sup['list_det'].split(' ')
                det = ' '
                if len(list_det) != 0:
                    for d in list_det:
                        if d == '1':
                            det += '\nНожка стула'
                        elif d == '2':
                            det += '\nНожка стола'
                        elif d == '3':
                            det += '\nСпинка стула'
                        elif d == '4':
                            det += '\nСидение стула'
                        elif d == '5':
                            det += '\nБоковая планка стула'
                        elif d == '6':
                            det += '\nПеремычка стола'
                        elif d == '7':
                            det += '\nСтолешница в сборе'
                        elif d == '8':
                            det += '\nБоковая планка стола'
                        elif d == '9':
                            det += '\nСтолешница'
                        elif d == '10':
                            det += '\nФурнитура'

                mess = f'*{det}*'

                inline_key = InlineKeyboardMarkup(row_width=1)
                status_ship = 'Общение с клиентом'
                inline_key_b1 = InlineKeyboardButton(text='Зафиксировать детали', callback_data=f'obr3_{sup["id_sup"]}')
                inline_key_b2 = InlineKeyboardButton(text='Клиент решил сам', callback_data=f'obr0_{sup["id_sup"]}')
                inline_key.add(inline_key_b1).add(inline_key_b2)
                await message.answer(f'ID запроса: *{sup["id_sup"]}*'
                                     f'\nТип запроса: *{sup["word_0"]}*'
                                     f'\nДата обращения: *{sup["date_q"]}*'
                                     f'\n\nИмя: *{name_user}*'
                                     f'\nНомер телефона: *{phone_user}*'
                                     f'\nСсылка: [https://t.me/{link_tg}]'
                                     f'\nТовар: *{sup["word_3"]}*'
                                     f'\nГде был заказан: *{sup["word_4"]}*'
                                     f'\nДата производства: *{sup["word_6"]}*'
                                     f'\n\nВопрос: \n`{sup["text_q"]}`'
                                     f'\n\nАдрес пункта: `{sup["adress_client"]}`'
                                     f'\n\nСтатус: *{status_ship}*', reply_markup=inline_key, parse_mode='Markdown')
            elif 'Детали_' in selone(f"SELECT act_wood FROM users WHERE id_user = '{user}'", user)['act_wood']:
                id_sup = selone(f"SELECT act_wood FROM users WHERE id_user = '{user}'", user)['act_wood'].split("_")[1]
                update(f"UPDATE wood SET list_det = '{message.text}' WHERE id_sup = '{id_sup}'", user)
                update(f"UPDATE users SET act_wood = '' WHERE id_user = '{user}'", user)
                update(f"UPDATE wood SET status_ship = 'Детали' WHERE id_sup = '{id_sup}'", user)
                sup = selone(f"SELECT * FROM wood WHERE id_sup = '{id_sup}'", user)
                id_user = sup["id_user"]
                name_user = selone(f"SELECT word_1 FROM wood_users WHERE id_user = '{id_user}'", user)['word_1']
                phone_user = selone(f"SELECT word_2 FROM wood_users WHERE id_user = '{id_user}'", user)['word_2']
                link_tg = selone(f"SELECT link_tg FROM wood_users WHERE id_user = '{id_user}'", user)['link_tg']

                list_det = sup['list_det'].split(' ')
                det = ' '
                if len(list_det) != 0:
                    for d in list_det:
                        if d == '1':
                            det += '\nНожка стула'
                        elif d == '2':
                            det += '\nНожка стола'
                        elif d == '3':
                            det += '\nСпинка стула'
                        elif d == '4':
                            det += '\nСидение стула'
                        elif d == '5':
                            det += '\nБоковая планка стула'
                        elif d == '6':
                            det += '\nПеремычка стола'
                        elif d == '7':
                            det += '\nСтолешница в сборе'
                        elif d == '8':
                            det += '\nБоковая планка стола'
                        elif d == '9':
                            det += '\nСтолешница'
                        elif d == '10':
                            det += '\nФурнитура'

                mess = f'*{det}*'

                inline_key = InlineKeyboardMarkup(row_width=1)
                status_ship = 'Общение с клиентом'
                inline_key_b1 = InlineKeyboardButton(text='Передать в цех', callback_data=f'ship_{sup["id_sup"]}')
                inline_key_b2 = InlineKeyboardButton(text='Клиент решил сам', callback_data=f'obr0_{sup["id_sup"]}')
                inline_key.add(inline_key_b1).add(inline_key_b2)
                await message.answer(f'ID запроса: *{sup["id_sup"]}*'
                                     f'\nТип запроса: *{sup["word_0"]}*'
                                     f'\nДата обращения: *{sup["date_q"]}*'
                                     f'\n\nИмя: *{name_user}*'
                                     f'\nНомер телефона: *{phone_user}*'
                                     f'\nСсылка: [https://t.me/{link_tg}]'
                                     f'\nТовар: *{sup["word_3"]}*'
                                     f'\nГде был заказан: *{sup["word_4"]}*'
                                     f'\nДата производства: *{sup["word_6"]}*'
                                     f'\n\nВопрос: \n`{sup["text_q"]}`'
                                     f'\n\nАдрес пункта: `{sup["adress_client"]}`'
                                     f'\n\nДетали: *{mess}*'
                                     f'\n\nСтатус: *{status_ship}*', reply_markup=inline_key, parse_mode='Markdown')
            elif 'Заказа_' in selone(f"SELECT act_wood FROM users WHERE id_user = '{user}'", user)['act_wood']:
                await message.answer(text='Пришлите *QR заказа* документом .pdf!!!!')
            elif 'Поставки_' in selone(f"SELECT act_wood FROM users WHERE id_user = '{user}'", user)['act_wood']:
                await message.answer(text='Пришлите *QR поставки* документом .pdf!!!!')

            # Создать доставку
            elif message.text == markups.mp_menu_b6:
                res = 'date_' + 'Доставка'
                update(f"UPDATE users SET act_log = '{res}' WHERE id_user = '{user}'", user)
                inline_date = ReplyKeyboardMarkup(resize_keyboard=True)
                inline_date_b2 = f'{sk.date_tomorrow_create()}'
                menu_back_logistic = '📛 Отмена'
                inline_date.add(inline_date_b2).add(menu_back_logistic)
                await message.answer(text='Введите дату когда нужно выполнить заявку _(в формате 01.11.2023)_', reply_markup=inline_date)
            elif 'date_' in selone(f"SELECT act_log FROM users WHERE id_user = '{user}'", user)['act_log']:
                if len(message.text.split('.')) == 3 and len(message.text) == 10:
                    delta_1 = datetime.timedelta(hours=5)
                    delta_2 = datetime.timedelta(days=1)
                    now = datetime.datetime.now() + delta_1
                    tom = datetime.datetime.now() + delta_2

                    if ((int(message.text[0:2]) <= int(now.day)) and (int(message.text[3:5]) == int(now.month))) or (int(message.text[3:5]) < int(now.month)):
                        await message.answer(text='Вы можете указать дату начиная с завтрашнего дня:', reply_markup=markups.back_mp_menu)

                    elif (int(message.text[0:2]) == int(tom.day)) and (int(sk.time_create()[0:2]) > 21):
                        await message.answer(text='На завтра вы уже не можете создать заявку, укажите другую дату:', reply_markup=markups.back_mp_menu)

                    else:
                        th_res = selone(f"SELECT act_log FROM users WHERE id_user = '{user}'", user)['act_log']
                        sec_res = th_res + '_' + str(message.text)
                        first_res = sec_res.split('_')
                        del first_res[0]

                        newlist = selist(f"SELECT num_ship FROM shipping WHERE date_ship = '{message.text}'", user)
                        list_log = sorted(newlist, key=lambda d: d['num_ship'])
                        num_ship = 0
                        th_res = selone(f"SELECT act_log FROM users WHERE id_user = '{user}'", user)['act_log']
                        sec_res = th_res + '_' + str(message.text) + '_'+ str(num_ship)
                        first_res = sec_res.split('_')
                        del first_res[0]

                        inline_item = ReplyKeyboardMarkup(resize_keyboard=True)
                        inline_item_b1 = 'Растущий стол и стул 1'
                        inline_item_b2 = 'Растущий стол и стул 2'
                        inline_item_b3 = 'Наполнитель 15 кг'
                        inline_item_b4 = 'Парящие полки'
                        menu_back_logistic = '📛 Отмена'
                        inline_item.add(inline_item_b1).add(menu_back_logistic)

                        res = 'item_' + '_'.join(first_res)
                        update(f"UPDATE users SET act_log = '{res}' WHERE id_user = '{user}'", user)
                        await message.answer(
                            text='Выберите наименование наименование предметов или введите иное:',
                            reply_markup=inline_item)

                else:
                    await message.answer(text='Введите дату в формате 01.11.2023:', reply_markup=markups.back_mp_menu)
            elif 'item_' in selone(f"SELECT act_log FROM users WHERE id_user = '{user}'", user)['act_log']:
                th_res = selone(f"SELECT act_log FROM users WHERE id_user = '{user}'", user)['act_log']
                sec_res = th_res + '_' + str(message.text)
                first_res = sec_res.split('_')
                del first_res[0]

                res = 'count_' + '_'.join(first_res)
                update(f"UPDATE users SET act_log = '{res}' WHERE id_user = '{user}'", user)
                await message.answer(text='Введите количество:', reply_markup=markups.back_mp_menu)
            elif 'count_' in selone(f"SELECT act_log FROM users WHERE id_user = '{user}'", user)['act_log']:
                if message.text.isdigit():
                    th_res = selone(f"SELECT act_log FROM users WHERE id_user = '{user}'", user)['act_log']
                    sec_res = th_res + '_' + str(message.text)
                    first_res = sec_res.split('_')
                    del first_res[0]
                    res = 'we_' + '_'.join(first_res)
                    update(f"UPDATE users SET act_log = '{res}' WHERE id_user = '{user}'", user)
                    await message.answer(text='Укажите общий вес _(например 20кг. или 1т.)_:', reply_markup=markups.back_mp_menu)
                else:
                    await message.answer(text='Введите количество числом:', reply_markup=markups.back_mp_menu)
            elif 'we_' in selone(f"SELECT act_log FROM users WHERE id_user = '{user}'", user)['act_log']:
                th_res = selone(f"SELECT act_log FROM users WHERE id_user = '{user}'", user)['act_log']
                sec_res = th_res + '_' + str(message.text)
                first_res = sec_res.split('_')
                del first_res[0]

                inline_ad = ReplyKeyboardMarkup(resize_keyboard=True)
                inline_ad_b1 = 'Сафроновский проезд 6 (ФФ)'
                inline_ad_b2 = 'Силикатная 3 к3 (Мебельный цех)'
                menu_back_logistic = '📛 Отмена'
                inline_ad.add(inline_ad_b1).add(inline_ad_b2).add(menu_back_logistic)

                res = 'adressb_' + '_'.join(first_res)
                update(f"UPDATE users SET act_log = '{res}' WHERE id_user = '{user}'", user)
                await message.answer(text='Выберите адрес загрузки или введите иной:', reply_markup=inline_ad)
            elif 'adressb_' in selone(f"SELECT act_log FROM users WHERE id_user = '{user}'", user)['act_log']:
                th_res = selone(f"SELECT act_log FROM users WHERE id_user = '{user}'", user)['act_log']
                sec_res = th_res + '_' + str(message.text)
                first_res = sec_res.split('_')
                del first_res[0]

                if message.text == 'Сафроновский проезд 6 (ФФ)':
                    inline_phone = ReplyKeyboardMarkup(resize_keyboard=True)
                    inline_phone_b2 = '8-937-482-57-52 Фулфилмент'
                    menu_back_logistic = '📛 Отмена'
                    inline_phone.add(inline_phone_b2).add(menu_back_logistic)
                    res = 'phoneb_' + '_'.join(first_res)
                    update(f"UPDATE users SET act_log = '{res}' WHERE id_user = '{user}'", user)
                    await message.answer(text='Выберите контакт или введите иной:', reply_markup=inline_phone)
                elif message.text == 'Силикатная 3 к3 (Мебельный цех)':
                    inline_phone = ReplyKeyboardMarkup(resize_keyboard=True)
                    inline_phone_b1 = '8-986-702-18-15 Нурислам'
                    inline_phone_b2 = '8-987-351-37-49 Рамиль'

                    menu_back_logistic = '📛 Отмена'
                    inline_phone.add(inline_phone_b1).add(inline_phone_b2).add(menu_back_logistic)
                    res = 'phoneb_' + '_'.join(first_res)
                    update(f"UPDATE users SET act_log = '{res}' WHERE id_user = '{user}'", user)
                    await message.answer(text='Выберите контакт или введите иной:', reply_markup=inline_phone)
                else:
                    res = 'phoneb_' + '_'.join(first_res)
                    update(f"UPDATE users SET act_log = '{res}' WHERE id_user = '{user}'", user)
                    await message.answer(text='Введите номер телефона и имя:', reply_markup=markups.back_mp_menu)
            elif 'phoneb_' in selone(f"SELECT act_log FROM users WHERE id_user = '{user}'", user)['act_log']:
                th_res = selone(f"SELECT act_log FROM users WHERE id_user = '{user}'", user)['act_log']
                sec_res = th_res + '_' + str(message.text)
                first_res = sec_res.split('_')
                del first_res[0]

                inline_tm = ReplyKeyboardMarkup(resize_keyboard=True)
                inline_tm_b2 = 'до 14:00'
                inline_tm_b3 = 'до 15:00'
                inline_tm_b4 = 'до 16:00'
                inline_tm_b5 = 'до 17:00'
                menu_back_logistic = '📛 Отмена'
                inline_tm.add(inline_tm_b2, inline_tm_b3).add(inline_tm_b4, inline_tm_b5).add(menu_back_logistic)

                res = 'timeship_' + '_'.join(first_res)
                update(f"UPDATE users SET act_log = '{res}' WHERE id_user = '{user}'", user)
                await message.answer(text='Выберите время до которого нужно доставить или введите иное:', reply_markup=inline_tm)
            elif 'timeship_' in selone(f"SELECT act_log FROM users WHERE id_user = '{user}'", user)['act_log']:
                th_res = selone(f"SELECT act_log FROM users WHERE id_user = '{user}'", user)['act_log']
                sec_res = th_res + '_' + str(message.text)
                first_res = sec_res.split('_')
                del first_res[0]

                inline_ad = ReplyKeyboardMarkup(resize_keyboard=True)
                menu_back_logistic = '📛 Отмена'
                inline_ad.add(menu_back_logistic)

                res = 'adressn_' + '_'.join(first_res)
                update(f"UPDATE users SET act_log = '{res}' WHERE id_user = '{user}'", user)
                await message.answer(text='Введите адрес покупателя (без номера квартиры):', reply_markup=inline_ad)
            elif 'adressn_' in selone(f"SELECT act_log FROM users WHERE id_user = '{user}'", user)['act_log']:
                th_res = selone(f"SELECT act_log FROM users WHERE id_user = '{user}'", user)['act_log']
                sec_res = th_res + '_' + str(message.text)
                first_res = sec_res.split('_')
                del first_res[0]

                if message.text == 'Сафроновский проезд 6 (Фулфилмент Центр Уфа)':
                    inline_phone = ReplyKeyboardMarkup(resize_keyboard=True)
                    inline_phone_b2 = '8-996-102-04-54 Ануар'
                    inline_phone_b4 = '8-995-948-29-00 Рахман'
                    menu_back_logistic = '📛 Отмена'
                    inline_phone.add(inline_phone_b2).add(inline_phone_b4).add(menu_back_logistic)
                    res = 'phonen_' + '_'.join(first_res)
                    update(f"UPDATE users SET act_log = '{res}' WHERE id_user = '{user}'", user)
                    await message.answer(text='Выберите контакт или введите иной:', reply_markup=inline_phone)
                elif message.text == 'Ленина 128 (CDEK)' or message.text == 'Бульвар Ибрагимова 35/1 (Яндекс Маркет)' or message.text == 'Комсомольская 15 (OZON)' or message.text == 'Карьерная 7 ст7 (OZON)' or message.text == 'Мокроусовская 8г (Wildberries)' or message.text == 'Электрозаводская 2А (Wildberries)':
                    res = 'comment_' + '_'.join(first_res) + '_Нет номера'
                    update(f"UPDATE users SET act_log = '{res}' WHERE id_user = '{user}'", user)
                    await message.answer(text='Укажите дополнительный комментарий:', reply_markup=markups.back_mp_menu)
                elif message.text == 'Силикатная 3 к3 (Мебельный цех)':
                    inline_phone = ReplyKeyboardMarkup(resize_keyboard=True)
                    inline_phone_b1 = '8-986-702-18-15 Нурислам'
                    inline_phone_b2 = '8-987-351-37-49 Рамиль'

                    menu_back_logistic = '📛 Отмена'
                    inline_phone.add(inline_phone_b1).add(inline_phone_b2).add(menu_back_logistic)
                    res = 'phonen_' + '_'.join(first_res)
                    update(f"UPDATE users SET act_log = '{res}' WHERE id_user = '{user}'", user)
                    await message.answer(text='Выберите контакт или введите иной:', reply_markup=inline_phone)
                elif message.text == 'Силикатная 24/1 (Упаковка)':
                    inline_phone = ReplyKeyboardMarkup(resize_keyboard=True)
                    inline_phone_b1 = '8-987-256-07-06 Роман'
                    inline_phone_b2 = '8-917-782-17-21 Айнур'

                    menu_back_logistic = '📛 Отмена'
                    inline_phone.add(inline_phone_b1).add(inline_phone_b2).add(menu_back_logistic)
                    res = 'phonen_' + '_'.join(first_res)
                    update(f"UPDATE users SET act_log = '{res}' WHERE id_user = '{user}'", user)
                    await message.answer(text='Выберите контакт или введите иной:', reply_markup=inline_phone)
                elif message.text == 'Силикатная 28Б (Офис)':
                    inline_phone = ReplyKeyboardMarkup(resize_keyboard=True)
                    inline_phone_b1 = '8-987-256-07-06 Роман'
                    inline_phone_b2 = '8-917-782-17-21 Айнур'

                    menu_back_logistic = '📛 Отмена'
                    inline_phone.add(inline_phone_b1).add(inline_phone_b2).add(menu_back_logistic)
                    res = 'phonen_' + '_'.join(first_res)
                    update(f"UPDATE users SET act_log = '{res}' WHERE id_user = '{user}'", user)
                    await message.answer(text='Выберите контакт или введите иной:', reply_markup=inline_phone)
                else:
                    res = 'phonen_' + '_'.join(first_res)
                    update(f"UPDATE users SET act_log = '{res}' WHERE id_user = '{user}'", user)
                    await message.answer(text='Введите номер телефона покупателя:', reply_markup=markups.back_mp_menu)
            elif 'phonen_' in selone(f"SELECT act_log FROM users WHERE id_user = '{user}'", user)['act_log']:
                th_res = selone(f"SELECT act_log FROM users WHERE id_user = '{user}'", user)['act_log']
                sec_res = th_res + '_' + str(message.text)
                first_res = sec_res.split('_')
                del first_res[0]

                res = 'comment_' + '_'.join(first_res)
                update(f"UPDATE users SET act_log = '{res}' WHERE id_user = '{user}'", user)
                await message.answer(text='Если нужна доставка до двери, то напишите подъезд и номер квартиры:', reply_markup=markups.back_mp_menu)
            elif 'comment_' in selone(f"SELECT act_log FROM users WHERE id_user = '{user}'", user)['act_log']:
                first_res = selone(f"SELECT act_log FROM users WHERE id_user = '{user}'", user)['act_log'].split('_')
                type_ship = first_res[1]
                date_ship = first_res[2]
                num_ship = first_res[3]
                item_ship = first_res[4]
                count_item_ship = first_res[5]
                w_ship = first_res[6]
                adress_begin = first_res[7]
                phone_begin = first_res[8]
                time_ship = first_res[9]
                adress_end = first_res[10]
                phone_end = first_res[11]
                comment_ship = message.text
                update(f"UPDATE users SET act_log = ' ' WHERE id_user = '{user}'", user)

                create(f"REPLACE INTO shipping(type_ship, date_ship, num_ship, item_ship, count_item_ship, w_ship, adress_begin, phone_begin, time_ship, adress_end, phone_end, comment_ship) VALUES ('{type_ship}', '{date_ship}', '{num_ship}', '{item_ship}', '{count_item_ship}', '{w_ship}', '{adress_begin}', '{phone_begin}', '{time_ship}', '{adress_end}', '{phone_end}', '{comment_ship}')", user)

                list_all_users = selist(f"SELECT * FROM users", user)
                list_user = []
                for us in list_all_users:
                    if 'log' in us['notif']:
                        list_user.append(us)

                for user1 in list_user:
                    try:
                        chat_id = str(user1["id_user"])
                        destination_bot = Bot(token='6490496152:AAHnBwfDRlUTyTFMOMGGCK6Eu3WejYpesIE')
                        await destination_bot.send_message(chat_id, f'*Новая заявка!*\n\n'
                                                                    f'Тип: *{type_ship}*\n'
                                                                    f'Дата: *{date_ship}*\n'
                                                                    f'Время: *{time_ship}*\n'
                                                                    f'Предмет: *{item_ship}*\n'
                                                                    f'Количество: *{count_item_ship}*\n'
                                                                    f'Вес: *{w_ship}*\n\n'
                                                                    f'Адрес загрузки: *{adress_begin}*\n'
                                                                    f'Адрес разгрузки: *{adress_end}*\n'
                                                                    f'Комментарий: *{comment_ship}*\n', parse_mode='Markdown')
                    except:
                        pass

                await message.answer(text='Заявка создана', reply_markup=markups.mp_menu)

            # Список доставок
            elif message.text == markups.mp_menu_b7:
                if len(selist(f"SELECT * FROM shipping WHERE (type_ship = 'Доставка' AND status_ship <> 'Отменен') AND (type_ship = 'Доставка' AND status_ship <> 'Закончен')", user)) != 0:
                    await message.answer(text='*Очередь заявок на доставку:*', reply_markup=markups.back_mp_menu)
                    newlist = selist(f"SELECT * FROM shipping WHERE (type_ship = 'Доставка' AND status_ship <> 'Отменен') AND (type_ship = 'Доставка' AND status_ship <> 'Закончен')", user)

                    list_log = sorted(newlist, key=lambda d: d['num_ship'])
                    for l in list_log:
                        inline_m = InlineKeyboardMarkup(row_width=2)
                        inline_m_b1 = InlineKeyboardButton(text='Отменить', callback_data=f'cancel_{l["id_ship"]}')
                        inline_m.add(inline_m_b1)
                        await message.answer(text=f'ID: *{l["id_ship"]}*\n'
                                                  f'Тип: *{l["type_ship"]}*\n'
                                                  f'Дата: *{l["date_ship"]}*\n'
                                                  f'Время: *{l["time_ship"]}*\n'
                                                  f'Предмет: *{l["item_ship"]}*\n'
                                                  f'Количество: *{l["count_item_ship"]}*\n'
                                                  f'Вес: *{l["w_ship"]}*\n\n'
                                                  f'Адрес загрузки: `{l["adress_begin"]}`\n'
                                                  f'Телефон загрузки: `{l["phone_begin"]}`\n'
                                                  f'Адрес разгрузки: `{l["adress_end"]}`\n'
                                                  f'Телефон разгрузки: `{l["phone_end"]}`\n'
                                                  f'Комментарий: *{l["comment_ship"]}*\n\n'
                                                  f'Статус: *{l["status_ship"]}*', parse_mode='Markdown',
                                             reply_markup=inline_m)
                else:
                    await message.answer(text='Очередь пуста!')

            # Отгрузка товаров
            elif message.text == markups.mp_menu_b8:
                inline_key = ReplyKeyboardMarkup(resize_keyboard=True)
                inline_key_b1 = 'WB FBS'
                inline_key_b2 = 'OZON FBS'
                inline_key_b3 = 'ЯМ FBS'
                inline_key_b4 = 'WB FBO'
                inline_key_b5 = 'OZON FBO'
                menu_back_logistic = '📛 Отмена'
                inline_key.add(inline_key_b1, inline_key_b2).add(inline_key_b3, inline_key_b4).add(inline_key_b5, menu_back_logistic)

                res = 'otgr_'
                update(f"UPDATE users SET act_wood = '{res}' WHERE id_user = '{user}'", user)
                await message.answer(text='Куда отгружено?', reply_markup=inline_key)
            elif 'otgr_' in selone(f"SELECT act_wood FROM users WHERE id_user = '{user}'", user)['act_wood']:
                inline_key = ReplyKeyboardMarkup(resize_keyboard=True)
                inline_key_1 = 'Растущий стол и стул 1'
                inline_key_2 = 'Растущий стол и стул 2'
                inline_key_3 = 'Наполнитель 15 кг'
                inline_key_4 = 'Парящие полки'
                menu_back_logistic = '📛 Отмена'
                inline_key.add(inline_key_1).add(inline_key_2).add(inline_key_3).add(inline_key_4).add(menu_back_logistic)

                res = 'otgr4_' + message.text
                update(f"UPDATE users SET act_wood = '{res}' WHERE id_user = '{user}'", user)
                await message.answer(text='Выберите товар:', reply_markup=inline_key)
            elif 'otgr4_' in selone(f"SELECT act_wood FROM users WHERE id_user = '{user}'", user)['act_wood']:
                where_sk = selone(f"SELECT act_wood FROM users WHERE id_user = '{user}'", user)['act_wood'].split('_')[1]
                inline_key = ReplyKeyboardMarkup(resize_keyboard=True)
                menu_back_logistic = '📛 Отмена'
                inline_key.add(menu_back_logistic)

                res = 'otgr2_' + where_sk + '_' + message.text
                update(f"UPDATE users SET act_wood = '{res}' WHERE id_user = '{user}'", user)
                await message.answer(text='Сколько штук?', reply_markup=inline_key)
            elif 'otgr2_' in selone(f"SELECT act_wood FROM users WHERE id_user = '{user}'", user)['act_wood']:
                if message.text.isdigit():
                    where_sk = selone(f"SELECT act_wood FROM users WHERE id_user = '{user}'", user)['act_wood'].split('_')[1]
                    item_sk = selone(f"SELECT act_wood FROM users WHERE id_user = '{user}'", user)['act_wood'].split('_')[2]
                    if where_sk == 'WB FBO' or where_sk == 'OZON FBO':
                        inline_key = ReplyKeyboardMarkup(resize_keyboard=True)
                        menu_back_logistic = '📛 Отмена'
                        inline_key.add(menu_back_logistic)

                        res = 'otgr3_' + where_sk + '_' + item_sk + '_' + message.text
                        update(f"UPDATE users SET act_wood = '{res}' WHERE id_user = '{user}'", user)
                        await message.answer(text='Введите примечание _(напр. Куда уехало?)_:', reply_markup=inline_key)
                    else:
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
                        date_create = f'{day_edit}.{month_edit}.{now.year}'

                        name_list = f"Складской учет"

                        worksheet = sh.worksheet(name_list)

                        values_list = worksheet.col_values(2)
                        num_row = len(values_list) + 1

                        worksheet.update_cell(num_row, 2, date_create)
                        worksheet.update_cell(num_row, 3, "Фулфилмент")
                        worksheet.update_cell(num_row, 6, where_sk)
                        worksheet.update_cell(num_row, 9, "-")
                        worksheet.update_cell(num_row, 15, message.text)
                        worksheet.update_cell(num_row, 11, item_sk)
                        update(f"UPDATE users SET act_wood = ' ' WHERE id_user = '{user}'", user)
                        await message.answer(text='Готово!', reply_markup=markups.mp_menu)
                else:
                    await message.answer(text='Введите количество числом!')
            elif 'otgr3_' in selone(f"SELECT act_wood FROM users WHERE id_user = '{user}'", user)['act_wood']:
                where_sk = selone(f"SELECT act_wood FROM users WHERE id_user = '{user}'", user)['act_wood'].split('_')[1]
                item_sk = selone(f"SELECT act_wood FROM users WHERE id_user = '{user}'", user)['act_wood'].split('_')[2]
                count_sk = selone(f"SELECT act_wood FROM users WHERE id_user = '{user}'", user)['act_wood'].split('_')[3]
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
                date_create = f'{day_edit}.{month_edit}.{now.year}'

                name_list = f"Складской учет"

                worksheet = sh.worksheet(name_list)

                values_list = worksheet.col_values(2)
                num_row = len(values_list) + 1

                worksheet.update_cell(num_row, 2, date_create)
                worksheet.update_cell(num_row, 3, "Фулфилмент")
                worksheet.update_cell(num_row, 6, where_sk)
                worksheet.update_cell(num_row, 9, message.text)
                worksheet.update_cell(num_row, 15, count_sk)
                worksheet.update_cell(num_row, 11, item_sk)
                update(f"UPDATE users SET act_wood = ' ' WHERE id_user = '{user}'", user)
                await message.answer(text='Готово!', reply_markup=markups.mp_menu)

            # Не понятно
            else:
                await message.answer(text='Я вас не понял', reply_markup=markups.menu_admin)

if __name__ == '__main__':
    executor.start_polling(db, on_startup=startup, skip_updates=True)