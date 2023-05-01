import requests

def get_repos_stats(username: str) -> list[dict]:
    """Собирает статистику по репозиториям заданного пользователя на GitHub """
    response = requests.get(f'https://api.github.com/users/{username}/repos')
    if response.status_code == 200:
        repos = response.json()
        return repos
    else:
        print("Error:", response.status_code)
