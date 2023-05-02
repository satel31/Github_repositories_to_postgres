import os

from dotenv import load_dotenv

from src.functions import get_repos_stats
from src.postgres_db import PostgresDB


def main() -> None:
    """Основной интерфейс программы"""

    # Запрашиваем имя пользователя для поиска
    print('Введите имя пользователя на GitHub для получения информации по репозиториям')
    username: str = input()

    # Собираем статистику по репозиториям пользователя
    repos: list[dict] = get_repos_stats(username)

    # Загружаем данные для подключения к БД из локального файла env
    load_dotenv()

    db_config = {
        'user': os.getenv('user'),
        'password': os.getenv('password'),
        'host': os.getenv('host'),
        'port': os.getenv('port'),
        'dbname': os.getenv('dbname')
    }

    # Запрашиваем имя таблицы
    print('Введите имя таблицы')
    table_name: str = input()

    # Создаем экземпляр PostgresDB, при инициализации которого создаётся таблица
    db = PostgresDB(table_name=table_name, **db_config)
    # Сохраняем данные в БД
    db.insert_data_to_db(repos)
    print(f'Данные успешно записаны в таблицу {table_name}')

    # Экспортируем данные в файл JSON
    db.insert_data_to_json()
    print(f'Данные успешно записаны в файл {table_name}.json')

    # Запрашиваем про необходимость сортировки и ограничение количества результатов
    sorting: str = input('Хотите отсортировать данные? Да/нет ')
    limiting: str = input('Хотите ограничить количество результатов? Да/нет ')

    # Выводим данные в зависимости от ответов: отсортированные и ограниченные, отсортированные, ограниченные, все
    if sorting.lower() == 'да' and limiting.lower() == 'да':
        sort_by: str = input('Введите имя колонки для сортировки: title, owner, forks, language, repository_url')
        limit_to: int = int(input('Введите количество результатов'))
        data: list[dict] = db.read_db(sort_by, limit_to)

        for d in data:
            print(d)

    elif sorting.lower() == 'да':
        sort_by: str = input('Введите имя колонки для сортировки: title, owner, forks, language, repository_url')
        data: list[dict] = db.read_db(sort_by)

        for d in data:
            print(d)

    elif limiting.lower() == 'да':
        limit_to = int(input('Введите количество результатов'))
        data: list[dict] = db.read_db(limit_to)

        for d in data:
            print(d)

    else:
        data: list[dict] = db.read_db()

        for d in data:
            print(d)


if __name__ == '__main__':
    main()
