import telebot

from config import TOKEN

bot = telebot.TeleBot(TOKEN)

# Определяем вопросы и ответы
questions = {
    'Q1. What color do you like the most?': [('Red', 3), ('Green', 2), ('Blue', 1), ('Yellow', 0)],
    'Q2. What is your favorite drink?': [('Tea', 1), ('Coffee', 2), ('Coca-Cola', 3), ('Water', 0)],
    'Q3. What is your favorite animal?': [('Cat', 2), ('Dog', 3), ('Horse', 1), ('Bird', 0)]
}

# Определяем список ответов пользователей
answers = []

# Определяем текущий вопрос
current_question = None

total_weight = 0  # добавляем переменную в глобальную область видимости


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start_message(message):
    global current_question

    # Стартуем опрос
    current_question = 0
    send_question(message.chat.id)


# Обработчик ответа на вопрос
@bot.message_handler(content_types=['text'])
def handle_answer(message):
    global current_question, questions, answers

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

    # Если это был последний вопрос, выводим список ответов и завершаем работу опроса
    if current_question == len(questions) - 1:
        total_weight = sum(
            [questions[question][[a[0] for a in questions[question]].index(answer)][1] for question, answer in
             zip(questions.keys(), answers)])
        bot.send_message(message.chat.id, f'Poll completed. Total weight is: {total_weight}')

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

        current_question = None
        return

    # Выводим следующий вопрос
    current_question += 1
    send_question(message.chat.id)


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

        current_question = None
        return

    question = list(questions.keys())[current_question]
    possible_answers = [answer[0] for answer in questions[question]]

    # Создаем клавиатуру с вариантами ответов
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(*possible_answers)

    # Отправляем вопрос
    bot.send_message(chat_id, question, reply_markup=markup)


bot.polling(none_stop=True)\
