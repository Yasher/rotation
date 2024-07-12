#age = 66

#print ("hkjdfghk" + str(age) +"jfadh")

import telebot
from telebot import types # для указание типов
import config
#import config
import config
import db
import voting


bot = telebot.TeleBot(config.config['token'])


n=1


#@bot.message_handler(commands=['start', 'help'])

@bot.message_handler(commands=['start']) #создаем команду
#def send_welcome(message):
#	bot.reply_to(message, "Howdy, how are you doing?")
def start(message):
    print(message.text)
    tg_id = message.from_user.id
    if db.get_user_role(tg_id) == True:
        rkm = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width = 3)
        rkm.add(types.KeyboardButton("Период"), types.KeyboardButton("Выборы"), types.KeyboardButton("Запись \n результатов"), types.KeyboardButton("Подмена"))
        # global n
        # if n==1:
        #     n=0
        msg = bot.send_message(message.chat.id, "Привет " + str(tg_id), reply_markup=rkm)
        msg = bot.send_message(message.chat.id, "Вы администратор")
        #a=1
        bot.register_next_step_handler(msg, user_handler)

    else:
        bot.send_message(chat_id=message.chat.id, text=";fkdjgksdfgl;k")

    #msg = bot.send_message(message.chat.id, "Запись данных...")
    #bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id, text="Данные записаны!!!")
def user_handler (message):
    if (message.text == "Период"):
        period_text = db.get_current_period()
        msg = bot.send_message(message.chat.id, "Текущий период: " + period_text)
        markup1 = types.InlineKeyboardMarkup()
        markup1.add(types.InlineKeyboardButton("Да", callback_data="yes"))
        markup1.add(types.InlineKeyboardButton("Нет", callback_data= "no"))
        msg = bot.send_message(message.chat.id, "Обновить?", reply_markup = markup1)

    if (message.text == "Выборы"):
        ### Проверка пуста ли таблица vote, если не пуста, то сообщить (спросить перезаписать)
        voting.voting()
        print("Выборы проведены")
    if (message.text == "Запись \n результатов"):
        ###Проверка есть ли в history уже данные этой ротации
        if db.check_current_vote_in_history() == False:
            db.insert_voting_results_into_history()
            msg = bot.send_message(message.chat.id, "Данные записаны!")
            bot.register_next_step_handler(msg, user_handler)
        else:
            msg = bot.send_message(message.chat.id, "Данные уже есть в таблице!")   #### Сделаьб вопрос перезаписать или нет
            bot.register_next_step_handler(msg, user_handler)
    if (message.text == "Подмена"):
        print("Подмена")
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes":
        print("yes")
        msg = bot.send_message(call.message.chat.id, "Введите год XXXX")
        bot.register_next_step_handler(msg, year_input)
    else:
        print("no")


def year_input(message):
    global year
    year = message.text
    msg = bot.send_message(message.chat.id, "Введите месяц XX")
    bot.register_next_step_handler(msg, month_input)

def month_input (message):
    global month
    month = message.text
    db.update_period(year, month)
    bot.register_next_step_handler(message, user_handler)





bot.infinity_polling(none_stop=True)