## сделать проверку на то что tg_id из списка

#

import time

## предусмотреть, если юзер не нажмет кнопку, а напишет ченить

## try except

## если юзер нажимает /start  и данные в current по нему есть, то удалить данные в curent и пойти далее

import telebot
from telebot import types # для указание типов
import db
import config

bot = telebot.TeleBot(config.config['token'])



shifts = db.get_shifts() # получаем список кортежей [(id_смены, имя_смены, tg_id), (x,x,x) (y,y,y)]

choice = []
count_shifts = {} # словарь key - tg_id, value - количество смен
#tg_id = "111"

text_button = "Выбери смены 🙈:"

# v1
# def make_markup():
#     markup = types.InlineKeyboardMarkup()
#     for i in shifts:
#         # markup.add(types.InlineKeyboardButton(i[1], callback_data=str(i[0])+", '"+str(i[1])+"'"))
#         markup.add(types.InlineKeyboardButton(i[1], callback_data=i[0]))
#     return markup


def make_markup(tg_id):
    markup = types.InlineKeyboardMarkup()
    for i in shifts:
        if i[2] == str(tg_id):
            # markup.add(types.InlineKeyboardButton(i[1], callback_data=str(i[0])+", '"+str(i[1])+"'"))
            markup.add(types.InlineKeyboardButton(i[1], callback_data=i[0])) #callback_data - id_смены
    return markup
#
# def get_count_shift(tg_id)
#     for i in shifts:
#         if i[2] == str(tg_id):
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
    # for i in shifts:
    #     if i[2] == str(tg_id):
    #         shifts.remove(i)

def add_userdata_to_shifts(tg_id):
    usershifts = db.get_shifts(tg_id)
    global shifts
    shifts.extend(usershifts)

def delete_userdata_from_choice(tg_id):
    #global choice

    #####
    ## проблема Проходит не по всем элементам
    # for i in choice:
    #     if str(tg_id) in i:
    #         print(choice)
    #         choice.remove(i)
    #####
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










     # if choice[1] in choice:
    #         choice.remove()


    # global count_shifts
    #del count_shifts[tg_id]
    # count = 0
    # for i in shifts:
    #     if i[2] == str(tg_id):
    #         count = count + 1
    # #count_shifts.append([tg_id, count])
    # count_shifts[tg_id] = count

@bot.message_handler(commands=['start'])
def start(message):
    tg_id = message.from_user.id

    if db.get_person_id_from_tg_id(tg_id) == 0:
        bot.send_message(chat_id=message.chat.id, text="А кaзачок-то засланный!!!")
    else:

        if db.check_shifts_persons_count() == False:
            bot.send_message(chat_id=message.chat.id, text="Количество сотрудников != количеству смен!!!!!")
        else:


            db.delete_user_from_current(tg_id)
            delete_userdata_from_shifts(tg_id)
            add_userdata_to_shifts(tg_id)
            delete_userdata_from_choice(tg_id)

            get_count(tg_id)
            msg1 = bot.send_message(message.chat.id, text_button.format(message.from_user), reply_markup = make_markup(tg_id))

# @bot.message_handler(commands=['start']) #создаем команду


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

@bot.callback_query_handler(func=lambda call: True)   ### при нажатии на кнопку смены:
def callback_worker(call):

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



            print(choice)
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


### УБРАТЬ В IF
    msg4 = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                 text=text_button2, reply_markup=make_markup(tg_id))
    # markup = types.InlineKeyboardMarkup()
    # button1 = types.InlineKeyboardButton("20:30 - 8:30 ", callback_data="1")
    #
    # markup.add(button1)
    #
    # text_button = "Выбери смены 🙈:"
    # bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
    #                       text= text_button, reply_markup=markup)

#print(choice)
#print(tg_id)

bot.polling(none_stop=True)
