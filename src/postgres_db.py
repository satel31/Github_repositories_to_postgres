import json
import psycopg2


class PostgresDB:
    """Обеспечивает взаимодействие с базой данных Postgres"""

    def __init__(self, table_name: str, dbname: str, user: str, password: str, host: str = 'localhost', port: str = '5432') -> None:
        """При инициализации объекта создаётся соединение, курсор и таблица"""

        # Создаем соединение
        self.conn = psycopg2.connect(host=host, database=dbname, user=user, password=password, port=port)
        # Создаем курсор
        self.cur = self.conn.cursor()
        # Создаем автокоммит
        self.conn.autocommit = True

        # Создаем таблицу
        self.table_name: str = table_name
        self.create_table()

    def create_table(self) -> None:
        """Создаём таблицу в БД"""
        with self.conn:
            self.cur.execute(f"""
                CREATE TABLE {self.table_name} (
                    repository_id SERIAL PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    owner VARCHAR(255) NOT NULL,
                    forks INTEGER,
                    language VARCHAR(255),
                    repository_url TEXT
                )
            """)

    def insert_data_to_db(self, repositories: list[dict]) -> None:
        """Добавляем данные в таблицу в БД"""
        with self.conn:
            for repository in repositories:
                self.cur.execute(
                    f"""
                    INSERT INTO {self.table_name} (title, owner, forks, language, repository_url)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (repository['name'], repository['owner']['login'], repository['forks'],
                     repository['language'], repository['html_url'])
                    )

    def insert_data_to_json(self) -> None:
        """Считываем данные из БД и экспортируем в файл JSON"""
        # Задаём название файла по названию таблицы
        file = f'{self.table_name}.json'
        # Считываем данные из БД
        repos_dict: list[dict] = self.read_db()
        # Записываем данные в файл
        with open(file, 'a', encoding='utf-8') as f:
            json.dump(repos_dict, f, ensure_ascii=False)

    def read_db(self, sort_by: str = None, limit: int = None) -> list[dict]:
        """Получаем и возвращаем данные из таблицы с сортировкой и/или ограничением или без"""
        with self.conn:
            # Данные с сортировкой и ограничением
            if sort_by and limit:
                self.cur.execute(f"""SELECT * FROM {self.table_name} ORDER BY {sort_by} LIMIT {limit}""")
            # Данные только с сортировкой
            elif sort_by:
                self.cur.execute(f"""SELECT * FROM {self.table_name} ORDER BY {sort_by}""")
            # Данные только с ограничением
            elif limit:
                self.cur.execute(f"""SELECT * FROM {self.table_name} LIMIT {limit}""")
            # Все данные без сортировки
            else:
                self.cur.execute(f"""SELECT * FROM {self.table_name}""")
            repos_data: list[tuple] = self.cur.fetchall()
            repos_dict = []
            # Преобразуем данные в список словарей репозиториев
            for data in repos_data:
                repos_dict.append({'repository_id': data[0],
                                   'title': data[1],
                                   'owner': data[2],
                                   'forks': data[3],
                                   'language': data[4],
                                   'repository_url': data[5]
                                   })
        return repos_dict
