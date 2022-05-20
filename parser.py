from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent


def parser():
    """
    Собираем все задачи с первой страницы
    fl.ru в категории программирование
    """
    ua = UserAgent()
    headers = {
        'User-Agent': ua.random
    }
    url = 'https://www.fl.ru/projects/category/programmirovanie/#/'
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    tasks = soup.find_all('a', class_="b-post__link")
    work = []
    for task in tasks:
        task_name = task.get_text()
        href = task.get('href')
        work.append({
            'Задача': task_name,
            'Ссылка': 'https://www.fl.ru'+href
        })
    return work


def main():
    print(parser())


if __name__ == '__main__':
    main()
