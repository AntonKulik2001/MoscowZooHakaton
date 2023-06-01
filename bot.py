import telebot
from config import TOKEN

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = 'Викторина созданная для Хакатона Московского Зоопарка! Для того чтобы начать введите "/start".'

    bot.reply_to(message, text)

#  Test branch GitHub

bot.polling(none_stop=True)