import telebot
from token_safe import TOKEN
from extensions import help_hello_mess, check_message, create_db, create_values

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def handle_start(message):
    bot.reply_to(message, help_hello_mess)


@bot.message_handler(commands=['values'])
def handle_values(message):
    val_dict = create_db()
    bot.reply_to(message, create_values(val_dict))


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    answer = check_message(message.text)
    bot.reply_to(message, answer)


bot.polling(none_stop=True)
