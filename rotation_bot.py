import time
import telebot
from telebot import types # для указание типов
import db
import config
import voting

bot = telebot.TeleBot(config.config['token'], parse_mode='HTML')

shifts = db.get_shifts() # получаем список кортежей [(id_смены, имя_смены, tg_id), (x,x,x) (y,y,y)]

choice = []

count_shifts = {} # словарь key - tg_id, value - количество смен

text_button = "Выбери смены 🙈:"

hello = 0

def make_markup(tg_id):
    markup = types.InlineKeyboardMarkup()
    for i in shifts:
        if i[2] == str(tg_id):
            # markup.add(types.InlineKeyboardButton(i[1], callback_data=str(i[0])+", '"+str(i[1])+"'"))
            markup.add(types.InlineKeyboardButton(i[1], callback_data=i[0])) #callback_data - id_смены
    return markup

def delete_userdata_from_shifts(tg_id):
    global shifts
    i = 0
    while True:
        try:
            if str(tg_id) in shifts[i]:
                shifts.remove(shifts[i])
            else:
                i += 1
        except Exception as error:
            print(error)
            break

def add_userdata_to_shifts(tg_id):
    usershifts = db.get_shifts(tg_id)
    global shifts
    shifts.extend(usershifts)

def delete_userdata_from_choice(tg_id):

    global choice
    i = 0
    while True:
        try:
            if str(tg_id) in choice[i]:
                choice.remove(choice[i])
            else:
                i += 1
        except Exception as error:
            print(error)
            break

@bot.message_handler(commands=['start'])
def start(message):
    global tg_id
    tg_id = message.from_user.id

    if db.get_person_id_from_tg_id(tg_id) == 0:
        bot.send_message(chat_id=message.chat.id, text="А кaзачок-то засланный!!!")
    else:
#Кнопки меню
        rkm = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        if db.is_user_admin(tg_id) == True:
            rkm.add(types.KeyboardButton("/start"), types.KeyboardButton("Выбор смен"), types.KeyboardButton("Период"), types.KeyboardButton("Результат"),
                    types.KeyboardButton("Запись результатов"), types.KeyboardButton("Подмена"), types.KeyboardButton("История"), types.KeyboardButton("Я прожался"))

            global hello
            if hello == 0:
                msg = bot.send_message(message.chat.id, "Привет!", reply_markup=rkm)
                msg = bot.send_message(message.chat.id, "Вы администратор")
                hello = 1
            # a=1
            bot.register_next_step_handler(msg, user_handler)
            # user_handler(msg)
        else:
            rkm.add(types.KeyboardButton("/start"), types.KeyboardButton("Выбор смен"), types.KeyboardButton("Результат"), types.KeyboardButton("Я прожался"))
            msg = bot.send_message(message.chat.id, "Привет " + db.get_person_fio_from_tg_id(tg_id)[0], reply_markup=rkm)
            bot.register_next_step_handler(msg, user_handler)


# @bot.message_handler(commands=['start']) #создаем команду
def user_handler (message):
    msg = message
    if (message.text == "Период"):
        period_text = db.get_current_period("normal")
        msg = bot.send_message(message.chat.id, "Текущий период: " + period_text)
        markup = make_inline_markup_ifnotshifts("period")
        msg = bot.send_message(message.chat.id, "Обновить?", reply_markup = markup)
    elif (message.text == "Выборы"):
        if db.check_shifts_persons_count() == False:
            bot.send_message(chat_id=message.chat.id, text="Количество сотрудников != количеству смен!!!!!")
        else:
        ### Проверка пуста ли таблица vote, если не пуста, то сообщить (спросить перезаписать)
            if db.check_table_is_empty("vote") == True:
                voting.voting()
                msg = bot.send_message(message.chat.id, "Выборы проведены!")
                #bot.register_next_step_handler(msg, user_handler)
                user_handler(msg)
            else:
                msg = bot.send_message(message.chat.id, "Таблица выборов не пуста.")
                markup = make_inline_markup_ifnotshifts("vote")
                msg = bot.send_message(message.chat.id, "Обновить?", reply_markup=markup)

    elif (message.text == "Запись результатов"):
        ###Проверка есть ли в history уже данные этой ротации
        if db.check_current_vote_in_history() == False:
            db.insert_voting_results_into_history()
            msg = bot.send_message(message.chat.id, "Данные записаны!!")
            #bot.register_next_step_handler(msg, user_handler)
        else:
            markup = make_inline_markup_ifnotshifts("results")
            msg = bot.send_message(message.chat.id, "Данные уже есть в таблице!", reply_markup=markup)   #### Сделаьб вопрос перезаписать или нет
            #bot.register_next_step_handler(msg, user_handler)
    elif (message.text == "Подмена"):
        print("Подмена")
        msg = bot.send_message(message.chat.id, "Эта кнопка пока не работает 🤷‍♂️ ")
        #bot.register_next_step_handler(msg, user_handler)
    elif (message.text == "Выбор смен"):
        if db.check_shifts_persons_count() == False:
            bot.send_message(chat_id=message.chat.id, text="Количество сотрудников != количеству смен!!!!!")
        else:
            #global tg_id
            db.delete_user_from_current(message.from_user.id)
            delete_userdata_from_shifts(message.from_user.id)
            add_userdata_to_shifts(message.from_user.id)
            delete_userdata_from_choice(message.from_user.id)
            get_count(message.from_user.id)
            msg1 = bot.send_message(message.chat.id, text_button.format(message.from_user), reply_markup=make_markup(message.from_user.id))
    elif (message.text == "История"):
        msgtext = make_msgtext_history()
        bot.send_message(message.chat.id, msgtext)
        markup = make_inline_markup_ifnotshifts("history")
        msg = bot.send_message(message.chat.id, "Удалить строку?", reply_markup=markup)
    elif (message.text == "Результат"):
        if db.check_shifts_persons_count() == False:
            bot.send_message(chat_id=message.chat.id, text="Количество сотрудников != количеству смен!!!!!")
        else:
            voting.voting()

            msgtext = make_msgtext_results()
            bot.send_message(message.chat.id, msgtext)
            markup = make_inline_markup_ifnotshifts("scheme")
            msg = bot.send_message(message.chat.id, "Показать схему выдачи смен?", reply_markup=markup)

        #bot.send_message(db.get_admin_tg_id(), "Привет от бота")

    elif (message.text == "Я прожался"):
        tg_id = msg.from_user.id
        db.enter_data_by_user(tg_id)
        bot.send_message(message.chat.id, "Молодец!")
        if all_entered_data():
            if db.check_settings_admin_msg() == False:
                bot.send_message(db.get_admin_tg_id(), make_msgtext_results())
                db.set_admin_msg(True)


        if db.is_user_admin(tg_id) == True:
            list_entered_print = ""
            list_not_entered_print = ""
            messagetext = ""
            num = 0
            list_entered = db.get_users_entered_data(True)
            for person in list_entered:
                list_entered_print += person[0] + "\n"
                num += 1
            list_not_entered = db.get_users_entered_data(False)
            for person in list_not_entered:
                list_not_entered_print += person[0] + "\n"
            num_p = db.get_person_count(False)
            if  num_p == num:
                notif = "Прожаты ВСЕ: \n"
                messagetext = notif + list_entered_print
            else:
                notif = "Прожаты НЕ все: \n"
                messagetext = notif + list_entered_print + "\n\n Остались: \n" + list_not_entered_print



            bot.send_message(message.chat.id, messagetext)
    bot.register_next_step_handler(msg, user_handler)



def make_msgtext_results():
    msgtext = ""
    result = db.get_voting_table()
    for l in result:
        msgtext += l[0] + "\t\t\t\t\t\t" + l[1] + "\n"

    #num = db.get_person_count(True)
    #num_p = db.get_person_count(False)
    if all_entered_data():
        msgtext = "<b>ИТОГОВЫЕ РЕЗУЛЬТАТЫ </b> на период " + str(db.get_current_period("normal_print")) + ": \n" + msgtext

    else:
        msgtext = "<b>ПРОМЕЖУТОЧНЫЕ РЕЗУЛЬТАТЫ</b>на период " + str(db.get_current_period("normal_print")) + ": \n" + msgtext

    return msgtext

def all_entered_data():
    num = db.get_person_count(True)
    num_p = db.get_person_count(False)
    if num_p == num:
        return True
    else:
        return False


def make_msgtext_history(id = 0):
    msgtext = ""
    period_text = db.get_current_period("curr_period_base")
    #period1 = db.get_current_period("curr_period_base")
    #period2 = db.get_current_period("curr_period+1_base")
    result = db.get_history(id)
    num=1
    for l in result:
        #msgtext += str(num) + ". " + l[0] + "\t" + l[1] + "\t" + l[2] + "\n"
        msgtext += str(l[0]) + "\t" + l[1] + "\t" + l[2] + "\t" + l[3] + "\n"
        num+=1
    #num = db.get_person_count(True)
    #num_p = db.get_person_count(False)
    if id == 0:
        msgtext = "<b>История за период " + period_text +":</b>\n" + msgtext
    else:
        msgtext = "Удаляем? " + msgtext

    return msgtext

def all_entered_data():
    num = db.get_person_count(True)
    num_p = db.get_person_count(False)
    if num_p == num:
        return True
    else:
        return False

def make_inline_markup_ifnotshifts(part):
    markup = types.InlineKeyboardMarkup()
    if part != "results":
        markup.add(types.InlineKeyboardButton("Да", callback_data="yes_" + str(part)))
        markup.add(types.InlineKeyboardButton("Нет", callback_data= "no_" + str(part)))
    elif part == "results":
        markup.add(types.InlineKeyboardButton("Удалить", callback_data="del_" + str(part)))
    return markup

def year_input(message):
    global year
    year = message.text
    msg = bot.send_message(message.chat.id, "Введите месяц XX")
    bot.register_next_step_handler(msg, month_input)


def month_input (message):
    global month
    month = message.text
    db.update_period(year, month)
    msg = bot.send_message(message.chat.id, "Новый период: " + str(month) + "." + str(year))
    db.clear_entered_data_in_person()
    db.set_admin_msg(False)

def del_str_history (message):
    msgtext = make_msgtext_history(message.text)
    global history_id
    history_id = message.text
    markup = make_inline_markup_ifnotshifts("history_del")
    bot.send_message(message.chat.id, msgtext, reply_markup=markup)

def get_count (tg_id):
    count = 0
    for i in shifts:
        if i[2] == str(tg_id):
            count = count + 1
    # count_shifts.append([tg_id, count])
    try:
        del count_shifts[tg_id]
    except:
        ""
    count_shifts[tg_id] = count
    print("count_shifts")
    print(count_shifts)

def send_scheme_tg (chat_id):
    with open("scheme.txt", "r") as file:
        bot.send_document(chat_id, file, visible_file_name="scheme.txt")

@bot.callback_query_handler(func=lambda call: True)   ### при нажатии на кнопку смены:
def callback_worker(call):

    if call.data == "yes_period":
        print("yes_period")
        msg = bot.send_message(call.message.chat.id, "Введите год XXXX")
        bot.register_next_step_handler(msg, year_input)
    elif call.data == "no_period":
        print("no_period")
        msg = bot.send_message(call.message.chat.id, "Изменения отклонены")
    elif call.data == "yes_history":
        msg = bot.send_message(call.message.chat.id, "Введите номер строки для удаления")
        bot.register_next_step_handler(msg, del_str_history)
    elif call.data == "no_history":
        msg = bot.send_message(call.message.chat.id, "Изменения отклонены")
    elif call.data == "yes_history_del":
        db.del_str_history(history_id)
        msg = bot.send_message(call.message.chat.id, "Строка удалена из базы")
    elif call.data == "no_history_del":
        msg = bot.send_message(call.message.chat.id, "Изменения отклонены")
    elif call.data == "yes_vote":
        voting.voting()
        msg = bot.send_message(call.message.chat.id, "Выборы проведены!")
    elif call.data == "no_vote":
        msg = bot.send_message(call.message.chat.id, "Изменения отклонены")
    elif call.data == "del_results":
        db.del_results_from_history()
        msg = bot.send_message(call.message.chat.id, "Данные удалены из истории")
    elif call.data == "yes_scheme":
        send_scheme_tg(call.message.chat.id)
        #msg = bot.send_message(call.message.chat.id, "Ща")
        #db.del_str_history(history_id)
        #msg = bot.send_message(call.message.chat.id, "Строка удалена из базы")
    elif call.data == "no_scheme":
        msg = bot.send_message(call.message.chat.id, "Понял Принял")
    else:
        tg_id = call.from_user.id
        text_button1=""
        text_button2=""
        # for item in shifts:         # обходим все смены разрешенные сотрудникам
        i=0
        while True:
            try:
                if (str(shifts[i][0]) == call.data) and (shifts[i][2] == str(tg_id)): #если в списке разреш смен встречаем смену сотрудника и кнопка этой смены нажата
                    #choice_str = [item[0], str(tg_id)]
                    global choice
                    choice.append((shifts[i][0], str(tg_id))) # пишем в список [id_смены, tg_id]
                    shifts.remove(shifts[i]) #удаляем из списка разреш смен выбранную смену
                    count_shifts[tg_id]-=1  #  уменьшаем количество невыбранных смен сотрудника
                    print(count_shifts)
                    if count_shifts[tg_id] == 0: # если невыбранных не осталось
                        #msg = bot.send_message(chat_id=call.message.chat.id, text="Запись данных...")
                        text_button1 = "Запись данных..."
                        msg2 = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text_button1)
                        db.insert_choice(choice, tg_id)
                        time.sleep(0.5)
                        text_button1 = "Данные записаны в базу!!!"
                        msg3 = bot.edit_message_text(chat_id=call.message.chat.id, message_id=msg2.message_id, text=text_button1)


                        chosen = db.get_chosen_shift(tg_id)
                        message_chosen=""
                        n_ch = 1
                        for sh in chosen:
                            print(sh[1])
                            message_chosen += str(n_ch) + ". " + sh[1] + "\n"
                            n_ch += 1
                        msg5 = bot.send_message(chat_id=call.message.chat.id, text=message_chosen)
                        # global choice
                        #msg6 = bot.send_message(chat_id=call.message.chat.id, text="Это ваш окончательный выбор?", reply_markup=make_inline_markup_ifnotshifts("final_choice"))
                        bot.send_message(chat_id=call.message.chat.id, text="Нажми \"Я прожался\", если это твой окончательный выбор.")
                else:
                    i += 1
            except Exception as error:
                print(error)
                break
                # while True:
                #     try:
                #         if str(tg_id) in choice[i]:
                #             choice.remove(choice[i])
                #         else:
                #             i += 1
                #     except Exception as error:
                #         print(error)
                #         break



    #            print(choice)
                # if bool(shifts) != True:
                #     db.insert_choice(choice, tg_id)

                    # print("shifts 0 - " + str(len(shifts)))
             #   print("y")
            #else:
             #   print("n")
        #print(shifts)

        # print("sss = " + str(sss))
        # print(tg_id)

        if text_button1 == "Данные записаны в базу!!!":
            text_button2 = "Данные записаны в базу!!!"
        else:
            text_button2 = text_button

        msg4 = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                     text=text_button2, reply_markup=make_markup(tg_id))


while True:
    try:
        bot.infinity_polling(timeout=10, long_polling_timeout = 5)
    except RequestException as err:
        print(err)
        print('* Connection failed, waiting to reconnect...')
        time.sleep(15)
        print('* Reconnecting.')
#bot.polling(none_stop=True)
