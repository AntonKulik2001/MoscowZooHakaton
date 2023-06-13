import telebot

from telebot import types
from config import TOKEN, contact, FEEDBACK

bot = telebot.TeleBot(TOKEN)

# Определяем вопросы и ответы
questions = {
    'Q1. Какой климат тебе больше нравится?': [('Жаркий', 3), ('Холодный', 2), ('Умеренный', 1)],
    'Q2. Как ты относишься к воде?': [('Буквально живу в ней', 1), ('Бррр, уберите её подальше от меня', 2)],
    'Q3. Что тебе сниться по ночам?': [('Рассекаю небесное пространство', 2), ('Дикая охота на дичь', 3), ('Представляю как сплю в тени', 1)]
}

# Определяем список ответов пользователей
answers = []

# Определяем текущий вопрос
current_question = 0

total_weight = 0  # добавляем переменную в глобальную область видимости

# Функция отправки вопроса
def send_question(chat_id):
    global current_question, questions

    # Ищем следующий вопрос, на который пользователь еще не ответил
    while current_question < len(questions):
        # Если ответ на вопрос уже есть в списке ответов, переходим к следующему вопросу
        if list(questions.keys())[current_question] in [answer.split('. ')[0] for answer in answers]:
            current_question += 1
        else:
            break

    # Если это был последний вопрос, завершаем опрос
    if current_question == len(questions):
        total_weight = sum(
            [questions[question][[a[0] for a in questions[question]].index(answer)][1] for question, answer in
             zip(questions.keys(), answers)])
        bot.send_message(chat_id, f'Poll completed. Total weight is: {total_weight}')

        # Выводим шкалу
        weights = {answer: 0 for answers in questions.values() for answer, weight in answers}
        for answer in answers:
            found = False
            for possible_answers in questions.values():
                for possible_answer, weight in possible_answers:
                    if possible_answer == answer:
                        weights[answer] += weight
                        found = True
                        break
                if found:
                    break
        for answer, weight in weights.items():
            print(f'{answer}: {weight}')

        current_question = 0
        return

    question = list(questions.keys())[current_question]
    possible_answers = [answer[0] for answer in questions[question]]

    # Создаем клавиатуру с вариантами ответов
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(*possible_answers)

    # Отправляем вопрос
    bot.send_message(chat_id, question, reply_markup=markup)

@bot.message_handler(commands=['help'])
def start(message: telebot.types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Викторина')
    btn2 = types.KeyboardButton('Оставить отзыв')
    btn3 = types.KeyboardButton('Узнать подробнее')
    text = f'Привет {message.chat.username}! Предлагаю тебе пройти викторину и узнать свое тотемное животное'
    markup.add(btn1,btn2,btn3)

    bot.send_message(message.chat.id, text, reply_markup=markup)

# Обработчик ответа на вопрос
@bot.message_handler(content_types=['text'])
def handle_answer(message: telebot.types.Message):
    global current_question, questions, answers

    question = list(questions.keys())[current_question]
    possible_answers = [answer[0] for answer in questions[question]]

    if message.text == 'Викторина':

        send_question(message.chat.id)

    elif message.text in possible_answers:

        # Получаем текущий вопрос и возможные ответы на него
        question = list(questions.keys())[current_question]
        possible_answers = [answer[0] for answer in questions[question]]

        # Если ответ пользователя не является возможным ответом, выводим ошибку
        if message.text not in possible_answers:
            bot.send_message(message.chat.id, 'Извините, я вас не понимаю')
            send_question(message.chat.id)  # повторно отправляем вопрос
            return

        # Добавляем ответ пользователя в список и суммируем его вес
        answer_index = possible_answers.index(message.text)
        answer = questions[question][answer_index][0]
        weight = questions[question][answer_index][1]
        answers.append(answer)

        # Выводим следующий вопрос
        current_question += 1
        send_question(message.chat.id)


    elif message.text == 'Оставить отзыв':
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('Оставить отзыв', url=FEEDBACK)
        markup.add(btn1)

        bot.reply_to(message, text='Перейдите по сслыку чтобы оставить отзыв', reply_markup=markup)

    elif message.text == 'Узнать подробнее':
        bot.reply_to(message, text=f'Для получения подробной информации вы можете связаться с этим человеком {contact}')


bot.polling(none_stop=True)