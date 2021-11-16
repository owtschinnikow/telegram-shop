import telebot
from token_code import TOKEN

"""
Возможные библиотеки
AIOGram
python-telegram-bot
Telepot
Telegram Bot Service
telebot
twx.botapi
pyTelegramBotAPI
"""


bot = telebot.TeleBot(TOKEN)  # Инициализация определённого бота по TOKEN


@bot.message_handler(commands=['help'])
def send_welcome(message):
    """
    Функция здоровается с пользователем при вводе команд 'start'
    :param message: сообщение от пользователя
    :return:
    """
    user_message = message.text
    user_id = message.chat.id
    commatd_list = ['/help - помощь по командам чата',
                    '/start - приветствие бота',
                    '/buy + <товар> - положить <товар> в корзину',
                    '/cart - вывести список покупок',
                    '/id - id пользователя']
    bot.send_message(message.chat.id, '\n '.join(commatd_list))
    print(user_id, message.chat.first_name, user_message)  # подглядывание


@bot.message_handler(commands=['id'])
def send_id(message):
    """
    Функция выдаёт ID пользователя
    :param message: сообщение от пользователя
    :return:
    """
    user_message = message.text
    user_id = message.chat.id
    answer_message = 'Ваш ID: ' + str(user_id)
    bot.send_message(message.chat.id, answer_message)
    print(user_id, message.chat.first_name, user_message)  # подглядывание


@bot.message_handler(commands=['start'])
def send_welcome(message):
    """
    Функция здоровается с пользователем при вводе команд 'start', 'help'
    :param message: сообщение от пользователя
    :return:
    """
    user_message = message.text
    user_id = message.chat.id
    bot.send_message(message.chat.id, "Hello! Делайте заказы!")
    print(user_id, message.chat.first_name, user_message)  # подглядывание


cart = {}

@bot.message_handler(commands=['buy'])
def buy_item(message):
    """
    Функция собирает покупки пользователей в корзину
    :param message: сообщение от пользователя
    :return:
    """
    user_message = message.text
    user_id = message.chat.id
    parsed_message = user_message.split()
    item = parsed_message[1]
    if user_id not in cart:
        cart[user_id] = []
    cart[user_id].append(item)
    answer_message = ('Товар ' + item + ' добавлен в корзину для ')
    bot.send_message(user_id, answer_message)
    print(user_id, message.chat.first_name, user_message)  # подглядывание


@bot.message_handler(commands=['cart'])
def buy_item(message):
    """
    Функция сообщает список покупок в корзине
    :param message: сообщение от пользователя
    :return:
    """
    user_message = message.text
    user_id = message.chat.id
    items = cart[user_id]
    answer_message = (str(message.chat.first_name) + '. Ваша корзина: ' + ', '.join(items) )
    bot.send_message(user_id, answer_message)
    print(user_id, message.chat.first_name, user_message)  # подглядывание

@bot.message_handler(commands=[''])
def admin_function(message):
    user_id = message.chat.id
    bot.send_message(user_id, message.chat.first_name)
    bot.send_message(user_id, message)
    print(message.chat.first_name, message.text)
    print(message.from_user.username, message.text)


bot.polling()  # Запуск бота