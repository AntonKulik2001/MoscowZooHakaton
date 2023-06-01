import telebot
from telebot import types
from config import TOKEN

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Викторина')
    btn2 = types.KeyboardButton('Оставить отзыв')
    btn3 = types.KeyboardButton('Узнать подробнее')
    text = f'Здравствуй {message.chat.username}! Добро пожаловать в Московский Зоопарк тырпыры, предлагаем тебе пройти викторину и поучавствовать в' \
           'программе по опеке животных, для продолжения выбери соответсвующее действие'
    markup.add(btn1,btn2,btn3)

    bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.message_handler(content_types=['text'])
def func(message: telebot.types.Message):
    if message.text == 'Викторина':
        #тут идет код викторины, для нее вроде есть функция последовательности ответов в документации
        pass

    elif message.text == 'Оставить отзыв':
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('Оставить отзыв', url='https://moscowzoo.ru/animals/')
        markup.add(btn1)

        bot.reply_to(message, text='Перейдите по сслыку чтобы оставить отзыв', reply_markup=markup)

    elif message.text == 'Узнать подробнее':
        contact = 'example@mail.ru'
        bot.reply_to(message, text=f'Для получения подробной информации вы можете связаться с этим человеком {contact}')


bot.polling(none_stop=True)