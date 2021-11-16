import telebot
try:
    from token_code import TOKEN
except:
    print('Извините, у вас нет доступа к токену спикера.')
    print('Сгенерируйте свой с помощью @BotFather и вставьте в следующую ячейку.')


bot = telebot.TeleBot(TOKEN)  # Инициализация определённого бота по TOKEN


class Item:
    """
    Класс для определения продуктов, количества и категорий в боте
    """
    def __init__(self, name='noname', quantity=0, category='unknown'):
        self.name = name
        self.quantity = quantity
        self.category = category

    def decrease(self):
        """
        Уменьшение позиции уменьшением на 1
        :return:
        """
        if self.quantity == 0:
            return 'fail'
        else:
            self.quantity = self.quantity - 1
            return self.quantity

    def increase(self):
        """
        Добавление позиции увеличением на 1
        :return:
        """
        self.quantity = self.quantity + 1
        return self.quantity


class Customer:
    """
    Класс для предоставления бонуса клиенту
    """
    def __init__(self, name='noname', bought_items=0, bonuses=0):
        self.name = name
        self.bought_items = bought_items
        self.bonuses = bonuses





# База данных склада с товарами. Словарь {product: [item1, item2, item3], ...}
warehouse = {'milk': Item('milk', 2, 'food'),
         'bread': Item('bread', 2, 'food'),
         'bear': Item('bear', 1, 'toys')}


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
    user_name = message.from_user.first_name
    if user_name is None:
        user_name = '<Скрытный пользователь :)>'
    answer_message = 'Hello, ' + user_name + 'Делайте заказы!'
    bot.send_message(message.chat.id, answer_message)
    print(user_id, message.chat.first_name, user_message)  # подглядывание


cart = {}  # База данных заказов пользователей с товарами. Словарь {user_id: [item1, item2], ...}
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
    if len(parsed_message) == 1:
        answer_message = 'Введите нужный товар после команды /buy'
        return bot.send_message(user_id, answer_message), print(user_id, message.chat.first_name, answer_message)
    item = parsed_message[1]
    # Проверяем, что товар есть в каталоге
    if item not in warehouse:
        answer_message = 'Товар ' + item + ' не продается, увы :('
        bot.send_message(message.chat.id, answer_message)
        return  print(user_id, message.chat.first_name, 'надо начать заказывать', item)
    # Проверяем, что товара достатоно на складе
    if warehouse[item].quantity <= 0:
        answer_message = 'Товар ' + item + ' закончился, скоро привезем!'
        bot.send_message(message.chat.id, answer_message)
        return  print(user_id, message.chat.first_name, 'надо заказать', item)
    # Все ок: уменьшаем число товаров на складе и добавляем его в корзину пользователя
    warehouse[item].decrease()
    if user_id not in cart:
        cart[user_id] = []
    cart[user_id].append(item)
    answer_message = ('Товар - ' + item + ' - добавлен в корзину для ')
    bot.send_message(user_id, answer_message)
    print(user_id, message.chat.first_name, user_message)  # подглядывание


@bot.message_handler(commands=['cart'])
def show_cart(message):
    """
    Функция сообщает список покупок в корзине
    :param message: сообщение от пользователя
    :return:
    """
    user_message = message.text
    user_id = message.chat.id
    if user_id not in cart:
        cart[user_id] = []
    items = cart[user_id]
    answer_message = (str(message.chat.first_name) + '. Ваша корзина: ' + ', '.join(items) )
    bot.send_message(user_id, answer_message)
    print(user_id, message.chat.first_name, user_message)  # подглядывание


@bot.message_handler(commands=['add'])
def show_warehouse(message):
    user_message = message.text
    user_id = message.chat.id
    parsed_message = user_message.split()
    if len(parsed_message) < 2:
        answer_message = 'После команды /add введите - название, количество, категорию'
        return bot.send_message(user_id, answer_message), print(user_id, message.chat.first_name, answer_message)
    item = parsed_message[1]
    # Если товара НЕТ в каталоге, то вставляем полную позицию - название, количество, категорию
    if len(parsed_message) == 4 and item not in warehouse:
        quantity = int(parsed_message[2])
        category = parsed_message[3]
        warehouse[item] = Item(item, quantity, category)
        show_warehouse(message)
        return  print(user_id, message.chat.first_name, 'добавлена позиция', item, quantity, category)
    # Если товара ЕСТЬ в каталоге
    # Количество ЕСТЬ, то увеличиваем на КОЛИЧЕСТВО.
    if item in warehouse:
        if len(parsed_message) == 3:
            quantity = int(parsed_message[2])
            warehouse[item].quantity += quantity
    #Количества нет, то увеличиваем на 1 шт.
        elif len(parsed_message) == 2:
            warehouse[item].increase()

    show_warehouse(message)

@bot.message_handler(commands=['warehouse'])
def show_warehouse(message):
    user_id = message.chat.id
    bot.send_message(user_id, 'Cостояние склада:')
    for k, v in warehouse.items():
        slot = (k, str(v.quantity), str(v.category))
        warehouse_slot = ' - '.join(slot)
        bot.send_message(user_id, warehouse_slot)


@bot.message_handler(commands=[''])
def admin_function(message):
    user_id = message.chat.id
    bot.send_message(user_id, message.chat.first_name)
    bot.send_message(user_id, message)
    print(message.chat.first_name, message.text)
    print(message.from_user.username, message.text)


bot.polling()  # Запуск бота