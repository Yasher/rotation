import telebot
import config

bot = telebot.TeleBot(config.config['token'])



@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.reply_to(message, message.text)

@bot.message_handler(content_types=['document', 'audio'])
def handle_docs_audio(message):
	bot.send_message(message, "Howdy, how are yo;fdgs,hl',srf,gthu doing?")

a="nenene"

@bot.edited_message_handler(func=lambda message: True)
def echo_all(message):
	bot.reply_to(message, "Howdyваыпваыпавы, how are you doing?")
	a = "dadada"
	print (a)


bot.infinity_polling()

print (a)