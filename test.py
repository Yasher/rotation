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
    if db.is_user_admin(tg_id) == True:
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
        period_text = db.get_current_period("normal")
        msg = bot.send_message(message.chat.id, "Текущий период: " + period_text)
        markup = make_inline_markup("period")
        #markup.add(types.InlineKeyboardButton("Да", callback_data="yes_period"))
        #markup.add(types.InlineKeyboardButton("Нет", callback_data= "no_period"))
        msg = bot.send_message(message.chat.id, "Обновить?", reply_markup = markup)

    if (message.text == "Выборы"):
        if db.check_shifts_persons_count() == False:
            bot.send_message(chat_id=message.chat.id, text="Количество сотрудников != количеству смен!!!!!")
        else:
        ### Проверка пуста ли таблица vote, если не пуста, то сообщить (спросить перезаписать)
            if db.check_table_is_empty("vote") == True:
                voting.voting()
                msg = bot.send_message(message.chat.id, "Выборы проведены!")
                bot.register_next_step_handler(msg, user_handler)
            else:
                msg = bot.send_message(message.chat.id, "Таблица выборов не пуста.")
                markup = make_inline_markup("vote")
                msg = bot.send_message(message.chat.id, "Обновить?", reply_markup=markup)

    if (message.text == "Запись \n результатов"):
        ###Проверка есть ли в history уже данные этой ротации
        if db.check_current_vote_in_history() == False:
            db.insert_voting_results_into_history()
            msg = bot.send_message(message.chat.id, "Данные записаны!")
            bot.register_next_step_handler(msg, user_handler)
        else:
            markup = make_inline_markup("results")
            msg = bot.send_message(message.chat.id, "Данные уже есть в таблице!", reply_markup=markup)   #### Сделаьб вопрос перезаписать или нет
            bot.register_next_step_handler(msg, user_handler)
    if (message.text == "Подмена"):
        print("Подмена")
        bot.register_next_step_handler(msg, user_handler)
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes_period":
        print("yes_period")
        msg = bot.send_message(call.message.chat.id, "Введите год XXXX")
        bot.register_next_step_handler(msg, year_input)
    elif call.data == "no_period":
        print("no_period")
        msg = bot.send_message(call.message.chat.id, "Изменения отклонены")
        bot.register_next_step_handler(msg, user_handler)
    elif call.data == "yes_vote":
        voting.voting()
        msg = bot.send_message(call.message.chat.id, "Выборы проведены!")
        bot.register_next_step_handler(msg, user_handler)
    elif call.data == "no_vote":
        msg = bot.send_message(call.message.chat.id, "Изменения отклонены")
        bot.register_next_step_handler(msg, user_handler)
    elif call.data == "del_results":
        print("удаляем")
        db.del_results_from_history()
    elif call.data == "update_results":
        print("перезаптсываем")

         ### доделать
        yyy




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
    bot.register_next_step_handler(message, user_handler)


def make_inline_markup(part):
    markup = types.InlineKeyboardMarkup()
    if part != "results":
        markup.add(types.InlineKeyboardButton("Да", callback_data="yes_" + str(part)))
        markup.add(types.InlineKeyboardButton("Нет", callback_data= "no_" + str(part)))
    elif part == "results":
        markup.add(types.InlineKeyboardButton("Удалить", callback_data="del_" + str(part)))
        markup.add(types.InlineKeyboardButton("Перезаписать", callback_data= "update_" + str(part)))
    return markup


bot.infinity_polling(none_stop=True)