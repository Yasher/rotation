import telebot
from telebot import types # для указание типов

# Обработчик команды /start
def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [
            InlineKeyboardButton("Нажми меня", callback_data='button_clicked'),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Привет! Нажми на кнопку ниже:', reply_markup=reply_markup)

# Обработчик нажатия кнопки
def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    # Изменяем текст сообщения
    query.edit_message_text(text="Сообщение изменено! Кнопка удалена.")

def main() -> None:
    # Замените 'YOUR_TOKEN' на токен вашего бота
    updater = Updater("YOUR_TOKEN")

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(button))

    # Запуск бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()