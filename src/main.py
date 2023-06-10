import os
from datetime import datetime, timedelta
from random import choice

import telebot

import utils


TOKEN = os.getenv('TO_DO_BOT_API')
HELP = '''/help - вывести список доступных команд
/add - добавить новую задачу в список в формате "/add - дата - задача"
/show - напечатать все добавленные задачи на заданную дату в формате "/show - дата"
/random - добавить случайную задачу на сегодняшнюю дату'''
RANDOM_TASKS = ["заказать еду", "посмотреть фильм", "почитать книгу", "сходить в ресторан", 'встретиться с друзьями',
                'завести кошку', 'завести собаку', 'выпить шампанского', 'разобрать шкаф', 'сходить на шоппинг',
                'устроить внеплановую тренировку']
PATH_TO_TASKS_FILE = 'tasks_file.json'

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["help"])
def get_help(message):
    """Отправляет справку в чат пользователю
    :param message: сообщение пользователя"""
    bot.send_message(message.chat.id, HELP)


@bot.message_handler(commands=['add'])
def add_task(message):
    """
    Отправляет сообщение пользователю о добавлении задачи
    :param message: запрос пользователя
    """
    command = message.text.split(' - ', maxsplit=2)

    try:
        date = command[1].lower()

        if date == 'сегодня':
            date = str(datetime.today().date())
        elif date == 'завтра':
            date = str(datetime.today().date() + timedelta(1))
        else:
            date = utils.get_processed_date(date)

        task = command[2]
        utils.add_todo(PATH_TO_TASKS_FILE, date, task)
        text = 'Задача ' + task + ' добавлена на дату ' + date
        bot.send_message(message.chat.id, text)

    except IndexError:
        bot.send_message(message.chat.id, 'Введите команду в верном формате "/add - дата - задача"')


@bot.message_handler(commands=['random'])
def add_random_task(message):
    """
    Отправляет сообщение пользователю о добавлении рандомной задачи
    :param message: запрос пользователя
    """
    date = str(datetime.now().date())
    task = choice(RANDOM_TASKS)

    utils.add_todo(PATH_TO_TASKS_FILE, date, task)

    text = 'Задача ' + task + ' добавлена на дату ' + date

    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['show'])
def show_tasks(message):
    """
    Отправляет сообщение пользователю с задачами на выбранную дату
    :param message: запрос пользователя
    """
    command = message.text.split(' - ', maxsplit=1)

    try:
        date = command[1].lower()

        if date == 'сегодня':
            date = str(datetime.today().date())
        elif date == 'завтра':
            date = str(datetime.today().date() + timedelta(1))
        else:
            date = utils.get_processed_date(date)

        tasks = utils.open_file_with_tasks(PATH_TO_TASKS_FILE)

        if date in tasks:
            text = date.upper() + '\n'

            for task in tasks[date]:
                text = text + '- ' + task + '\n'
        else:
            text = 'На данную дату нет доступных задач'

        bot.send_message(message.chat.id, text)

    except IndexError:
        bot.send_message(message.chat.id, 'Введите команду в верном формате "/show - дата"')


bot.polling(none_stop=True)
