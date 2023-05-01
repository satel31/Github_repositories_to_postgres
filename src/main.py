from src.functions import get_repos_stats
from src.postgres_db import PostgresDB

#собрать статистику по репозиториям пользователя
repos = get_repos_stats('satel31')

#сохранения данных в базу данных
PASSWORD = ''
db = PostgresDB(host='localhost', db_name='test', user='postgres', password=PASSWORD, table_name='test_gh')
db.insert_data_to_db(repos)

#экспортировать данные в формате JSON
db.insert_data_to_json()
print(db.read_db())
print(db.read_db('forks', 3))
print(db.read_db('forks'))
print(db.read_db(3))
