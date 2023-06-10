import json
import re
from datetime import datetime


MONTHS = {'января': 1, 'февраля': 2, 'марта': 3, 'апреля': 4, 'мая': 5, 'июня': 6, 'июля': 7, 'августа': 8,
          'сентября': 9, 'октября': 10, 'ноября': 11, 'декабря': 12}


def get_processed_date(date):
    """
    Возвращает отформатированную дату
    :param date: дата для форматирования
    :return: дата в нужном формате
    """
    date_in_list = re.findall(
        r'\d{2}.\d{2}.\d{4}|\d.\d{2}.\d{4}|\d{2} [яфмиасонд]\w+[яа] \d{4}|\d [яфмиасонд]\w+[яа] \d{4}', date)
    date = date_in_list[0]
    date = re.split(r'[:./\s]', date)

    try:
        date = str(datetime(int(date[2]), int(date[1]), int(date[0])).date())
    except ValueError:
        date = str(datetime(int(date[2]), MONTHS[date[1]], int(date[0])).date())

    return date


def add_todo(path, date, task):
    """
    Добавляет задачу в список дел
    :param path: путь к файлу с задачами
    :param date: дата для установки задачи
    :param task: задача
    """
    with open(path, 'r', encoding='utf-8') as tasks_file:
        tasks_text = tasks_file.read()

    tasks = json.loads(tasks_text)

    if date in tasks:
        tasks[date].append(task)
    else:
        tasks[date] = []
        tasks[date].append(task)

    tasks_text = json.dumps(tasks)

    with open(path, 'w', encoding='utf-8') as tasks_file:
        tasks_file.write(tasks_text)
