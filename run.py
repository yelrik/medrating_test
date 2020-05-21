import requests
import os
from datetime import datetime

# Делаем запросы по API и сохраняем результат в переменную
users = requests.get('https://json.medrating.org/users')
todos = requests.get('https://json.medrating.org/todos')

# Создаем пустой список для группировки пользователей и их задач
users_todos = []

# Проходим циклом по пользователям
for user in users.json():
    if 'name' in user:
        user_todos = {
            'user_name': user['name'],
            'user_id': user['id'],
            'user_email': user['email'],
            'user_company': user['company'],
            'user_tasks': []
        }
        tasks = []  # Список для задач пользователя

        # Перебираем список задач
        for todo in todos.json():
            #  Если id пользователя в задаче совпадает с id текущего пользователя
            if 'userId' in todo and todo['userId'] == user_todos['user_id']:
                # Выбираем нужные поля из задачи
                task = {
                    'task_id': todo['id'],
                    'task_title': todo['title'],
                    'task_completed': todo['completed']
                }
                # Добавляем задачу в список задач пользователя
                tasks.append(task)
        # Добавляем сформированный список задач пользователя
        user_todos['user_tasks'].extend(tasks)
    # Добавляем пользователя с его задачами в общий список пользователей
    users_todos.append(user_todos)

# Создаем папку для размещения отчета о задачах пользователей
try:
    os.mkdir('tasks')
except FileExistsError:
    print('Директория tasks уже существует')


def get_completed_tasks_names(tasks):
    completed_tasks = []
    for task in tasks:
        if task['task_completed'] == True:
            completed_tasks.append(task['task_title'])
    return completed_tasks


def get_uncompleted_tasks_names(tasks):
    completed_tasks = []
    for task in tasks:
        if task['task_completed'] == False:
            completed_tasks.append(task['task_title'])
    return completed_tasks


def write_users_task(user_data):
    completed_tasks = get_completed_tasks_names(user_data['user_tasks'])
    uncompleted_tasks = get_uncompleted_tasks_names(user_data['user_tasks'])
    with open('tasks/' + user_data['user_name'] + '.txt', 'w+') as file_handler:
        file_handler.write('{user_name} <{user_email}> {timestamp}\n'.format(
            user_name=user_data['user_name'],
            user_email=user_data['user_email'],
            timestamp=datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        ))
        file_handler.write('{user_company}\n\n'.format(
            user_company=user_data['user_company']['name']))
        file_handler.write('Завершенные задачи:\n')
        file_handler.writelines(task + '\n' for task in completed_tasks)
        file_handler.write('\nОставшиеся задачи:\n')
        file_handler.writelines(task + '\n' for task in uncompleted_tasks)


for user_todo in users_todos:
    write_users_task(user_todo)
