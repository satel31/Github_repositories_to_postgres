import json
import psycopg2


class PostgresDB:
    """Обеспечивает взаимодействие с базой данных Postgres"""

    def __init__(self, table_name: str, dbname: str, user: str, password: str, host: str = 'localhost', port: str = '5432'):
        self.conn = psycopg2.connect(host=host, database=dbname, user=user, password=password, port=port)
        self.cur = self.conn.cursor()
        self.conn.autocommit = True
        self.table_name: str = table_name

        self.create_table()

    def create_table(self):
        """Создать таблицу"""
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

    def insert_data_to_db(self, repositories: list[dict]):
        """Добавить данные в таблицу"""
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

    def insert_data_to_json(self):
        """Экспортировать данные в формат JSON"""
        file = f'{self.table_name}.json'
        repos_dict: list[dict] = self.read_db()
        with open(file, 'a', encoding='utf-8') as f:
            json.dump(repos_dict, f, ensure_ascii=False)

    def read_db(self, sort_by: str = None, limit: int = None):
        """Получить данные из таблицы."""
        with self.conn:
            if sort_by and limit:
                self.cur.execute(f"""SELECT * FROM {self.table_name} ORDER BY {sort_by} LIMIT {limit}""")
            elif sort_by:
                self.cur.execute(f"""SELECT * FROM {self.table_name} ORDER BY {sort_by}""")
            elif limit:
                self.cur.execute(f"""SELECT * FROM {self.table_name} LIMIT {limit}""")
            else:
                self.cur.execute(f"""SELECT * FROM {self.table_name}""")
            repos_data: list[tuple] = self.cur.fetchall()
            repos_dict = []
            for data in repos_data:
                repos_dict.append({'repository_id': data[0],
                                   'title': data[1],
                                   'owner': data[2],
                                   'forks': data[3],
                                   'language': data[4],
                                   'repository_url': data[5]
                                   })
        return repos_dict
