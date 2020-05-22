import requests
import os
from datetime import datetime
import re
import dateutil.parser
from functions import get_completed_tasks_names, get_timestamp_from_file, get_uncompleted_tasks_names, write_users_task

# Делаем запросы по API и сохраняем результат в переменную

try:
    users = requests.get('https://json.medrating.org/users')
    users.raise_for_status()
except requests.exceptions.ConnectionError as errc:
    print('Нет соединения с сервером. Проверьте интернет-подключение. Программа будет завершена.')
    raise SystemExit(errc)
except requests.exceptions.HTTPError as errh:
    print ("Ошибка в HTTP запросе:",errh)
    raise SystemExit(errh)
except requests.exceptions.Timeout as errt:
    print('Тайм-айт соединения...Программа будет завершена')
    raise SystemExit(errh)
except requests.exceptions.RequestException as err:
    print('Упс...что-то пошло нет так')
    raise SystemExit(err)

try:
    todos = requests.get('https://json.medrating.org/todos')
    todos.raise_for_status()
except requests.exceptions.ConnectionError as errc:
    print('Нет соединения с сервером. Проверьте интернет-подключение. Программа будет завершена.')
    raise SystemExit(errc)
except requests.exceptions.HTTPError as errh:
    print ("Ошибка в HTTP запросе:",errh)
    raise SystemExit(errh)
except requests.exceptions.Timeout as errt:
    print('Тайм-айт соединения...Программа будет завершена')
    raise SystemExit(errh)
except requests.exceptions.RequestException as err:
    print('Упс...что-то пошло нет так')
    raise SystemExit(err)  

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

# Перебираем список с пользователями и их задачами, формируем отчеты
for user_todo in users_todos:
    write_users_task(user_todo)
