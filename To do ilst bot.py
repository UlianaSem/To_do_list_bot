import telebot
from random import choice
from datetime import datetime
from datetime import timedelta
import re

token = ''
bot = telebot.TeleBot(token)
HELP = '''/help - вывести список доступных команд
/add - добавить новую задачу в список в формате "/add - дата - задача"
/show - напечатать все добавленные задачи на заданную дату в формате "/show - дата"
/random - добавлять случайную задачу на сегодняшнюю дату'''
tasks = {}
RANDOM_TASKS = ["заказать еду", "посмотреть фильм", "почитать книгу", "сходить в ресторан", 'встретиться с друзьями',
                'завести кошку', 'завести собаку', 'выпить шампанского', 'разобрать шкаф', 'сходить на шоппинг',
                'устроить внеплановую тренировку']
months = {'января': 1, 'февраля': 2, 'марта': 3, 'апреля': 4, 'мая': 5, 'июня': 6, 'июля': 7, 'августа': 8,
          'сентября': 9, 'октября': 10, 'ноября': 11, 'декабря': 12}


def date_processing(date):
    date_list = re.findall(
        r'\d{2}.\d{2}.\d{4}|\d.\d{2}.\d{4}|\d{2} [яфмиасонд]\w+[яа] \d{4}|\d [яфмиасонд]\w+[яа] \d{4}', date)
    date = date_list[0]
    date = re.split(r'[:./\s]', date)
    try:
        date = str(datetime(int(date[2]), int(date[1]), int(date[0])).date())
    except ValueError:
        date = str(datetime(int(date[2]), months[date[1]], int(date[0])).date())
    return date


def add_todo(date, task):
    if date in tasks:
        tasks[date].append(task)
    else:
        tasks[date] = []
        tasks[date].append(task)


@bot.message_handler(commands=["help"])
def reference(message):
    bot.send_message(message.chat.id, HELP)


@bot.message_handler(commands=['add'])
def add(message):
    command = message.text.split(' - ', maxsplit=2)
    date = command[1].lower()
    if date == 'сегодня':
        date = str(datetime.today().date())
    elif date == 'завтра':
        date = str(datetime.today().date() + timedelta(1))
    else:
        date = date_processing(date)
    task = command[2]
    add_todo(date, task)
    text = 'Задача ' + task + ' добавлена на дату ' + date
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['random'])
def random(message):
    date = str(datetime.now().date())
    task = choice(RANDOM_TASKS)
    add_todo(date, task)
    text = 'Задача ' + task + ' добавлена на дату ' + date
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['show'])
def show(message):
    command = message.text.split(' - ', maxsplit=1)
    date = command[1].lower()
    if date == 'сегодня':
        date = str(datetime.today().date())
    elif date == 'завтра':
        date = str(datetime.today().date() + timedelta(1))
    else:
        date = date_processing(date)
    if date in tasks:
        text = date.upper() + '\n'
        for task in tasks[date]:
            text = text + '- ' + task + '\n'
    else:
        text = 'На данную дату нет доступных задач'
    bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
