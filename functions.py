import requests
import os
from datetime import datetime
import re
import dateutil.parser


def get_completed_tasks_names(tasks):
    """
    Возвращает список с завершенными задачами пользователя
    """
    completed_tasks = []
    for task in tasks:
        if task['task_completed'] == True:
            completed_tasks.append(task['task_title'])
    return completed_tasks


def get_uncompleted_tasks_names(tasks):
    """
    Возвращает список с незавершенными задачами пользователя
    """
    completed_tasks = []
    for task in tasks:
        if task['task_completed'] == False:
            completed_tasks.append(task['task_title'])
    return completed_tasks


def get_timestamp_from_file(path):
    """
    Парсит 1ю строчку переданного файла, находит дату, возвращает ее в нужном формате
    """
    first_string = ''
    with open(path, 'r') as file_handler:
        first_string = file_handler.readlines()[0]
    timestamp = re.search(
        r'\d{2}\.\d{2}\.\d{4} \d{2}:\d{2}', first_string).group(0)
    timestamp_formated = dateutil.parser.parse(
        timestamp).strftime("%Y-%m-%dT%H:%M")
    return timestamp_formated


def write_users_task(user_data):
    """
    Записывает задачи пользователей в файлы на диске
    """
    completed_tasks = get_completed_tasks_names(user_data['user_tasks'])
    uncompleted_tasks = get_uncompleted_tasks_names(user_data['user_tasks'])
    path = 'tasks/' + user_data['user_name'] + '.txt'
    if os.path.isfile(path):
        formated_timestamp = get_timestamp_from_file(path)
        new_path = 'tasks/' + \
            user_data['user_name'] + '_' + formated_timestamp + '.txt'
        os.rename(path, new_path)

    with open(path, 'w+') as file_handler:
        file_handler.write('{user_name} <{user_email}> {timestamp}\n'.format(
            user_name=user_data['user_name'],
            user_email=user_data['user_email'],
            timestamp=datetime.now().strftime("%d.%m.%Y %H:%M")
        ))
        file_handler.write('{user_company}\n\n'.format(
            user_company=user_data['user_company']['name']))
        file_handler.write('Завершенные задачи:\n')
        file_handler.writelines(task + '\n' for task in completed_tasks)
        file_handler.write('\nОставшиеся задачи:\n')
        file_handler.writelines(task + '\n' for task in uncompleted_tasks)
