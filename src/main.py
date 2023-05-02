from src.functions import get_repos_stats
from src.postgres_db import PostgresDB
from dotenv import load_dotenv
import os

#собрать статистику по репозиториям пользователя
#repos = get_repos_stats('satel31')

#сохранения данных в базу данных
load_dotenv()

db_config = {
    'user': os.getenv('user'),
    'password': os.getenv('password'),
    'host': os.getenv('host'),
    'port': os.getenv('port'),
    'dbname': os.getenv('dbname')
}
db = PostgresDB(table_name='test_gh2', **db_config)
#db.insert_data_to_db(repos)

#экспортировать данные в формате JSON
#db.insert_data_to_json()
#print(db.read_db())
#print(db.read_db('forks', 3))
#print(db.read_db('forks'))
#print(db.read_db(3))

#if __name__ == '__main__':
    #main()