import os

from dotenv import load_dotenv

from src.functions import get_repos_stats
from src.postgres_db import PostgresDB


def main():
    # собрать статистику по репозиториям пользователя
    print('Введите имя пользователя на GitHub для получения информации по репозиториям')
    username = input()
    repos = get_repos_stats(username)

    # сохранения данных в базу данных
    load_dotenv()

    db_config = {
        'user': os.getenv('user'),
        'password': os.getenv('password'),
        'host': os.getenv('host'),
        'port': os.getenv('port'),
        'dbname': os.getenv('dbname')
    }
    print('Введите имя таблицы')
    table_name = input()
    db = PostgresDB(table_name=table_name, **db_config)
    db.insert_data_to_db(repos)
    print(f'Данные успешно записаны в таблицу {table_name}')

    # экспортировать данные в формате JSON
    db.insert_data_to_json()
    print(f'Данные успешно записаны в файл {table_name}.json')
    sorting = input('Хотите отсортировать данные? Да/нет ')

    limiting = input('Хотите ограничить количество результатов? Да/нет ')

    if sorting.lower() == 'да' and limiting.lower() == 'да':
        sort_by = input('Введите имя колонки для сортировки: title, owner, forks, language, repository_url')
        limit_to = input('Введите количество результатов')
        data = db.read_db(sort_by, limit_to)
        for d in data:
            print(d)
    elif sorting.lower() == 'да':
        sort_by = input('Введите имя колонки для сортировки: title, owner, forks, language, repository_url')
        data = db.read_db(sort_by)
        for d in data:
            print(d)
    elif limiting.lower() == 'да':
        limit_to = input('Введите количество результатов')
        data = db.read_db(limit_to)
        for d in data:
            print(d)
    else:
        data = db.read_db()
        for d in data:
            print(d)


if __name__ == '__main__':
    main()
