## сделать проверку на то что tg_id из списка

## предусмотреть, если юзер не нажмет кнопку, а напишет ченить

## try except

## если юзер нажимает /start  и данные в current по нему есть, то удалить данные в curent и пойти далее

import telebot
from telebot import types # для указание типов
import db
import config

bot = telebot.TeleBot(config.config['token'])

shifts = db.get_shifts()

choice = []
count_shifts = {}
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
            markup.add(types.InlineKeyboardButton(i[1], callback_data=i[0]))
    return markup
#
# def get_count_shift(tg_id)
#     for i in shifts:
#         if i[2] == str(tg_id):


@bot.message_handler(commands=['start']) #создаем команду
def start(message):
    tg_id = message.from_user.id

    # button1 = types.InlineKeyboardButton("20:30 - 8:30 ", callback_data = "1")
    # button2 = types.InlineKeyboardButton("8:30 - 20:30 ", callback_data = "2")
    # markup.add(button1)
    # markup.add(button2)
    # global sss
    # sss = 765
    count = 0
    for i in shifts:
        if i[2] == str(tg_id):
            count = count + 1
    #count_shifts.append([tg_id, count])
    count_shifts[tg_id] = count
    print (count_shifts)
    bot.send_message(message.chat.id, text_button.format(message.from_user), reply_markup = make_markup(tg_id))

# @bot.message_handler(commands=['start']) #создаем команду
# def start(message):

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):

   # choice.append(call.data)
   # print (choice)

    # global tg_id
    tg_id = call.from_user.id

    # print(shifts)
    # shifts.remove(call.data)
    # print(shifts)
    for item in shifts:
        #print(item[0])
        if (str(item[0]) == call.data) and (item[2] == str(tg_id)):
            choice_str = (item[0], str(tg_id))
            choice.append(choice_str)
            shifts.remove(item)
            count_shifts[tg_id]-=1
            print(count_shifts)
            if count_shifts[tg_id] == 0:
                bot.send_message(call.message.chat.id,  "jhksdflkgjsdhjfljkg")


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
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=text_button, reply_markup=make_markup(tg_id))

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
