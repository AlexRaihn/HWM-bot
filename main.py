import requests
from bs4 import BeautifulSoup
import re
import time
import random

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11) AppleWebKit/514.36 (KHTML, like Gecko) Chrome/79.0.2803.116',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Connection': 'keep-alive',
    'Accept-Language': 'ru-RU,ru;q=0.5,en-US;q=0.5,en;q=0.3'
}

your_login = '--Алиса--'
your_password = 'S631klxv'

s = requests.Session()
data_login = {
    'LOGIN_redirect': '1',
    'login': your_login.encode('windows-1251'),
    'lreseted': '1',
    'pass': your_password.encode('windows-1251'),
    'preseted': '1',
    'pliv': '15000',
    'x': '1',
    'y': '1'
}

s.post('https://www.heroeswm.ru/login.php', data=data_login, headers=HEADERS)

def ParseLinks(links, session, HEADERS):
    for url in links:
        full_url = f'https://www.heroeswm.ru/{url}'  # добавляем схему и домен к URL
        id_index = url.find('id=')  # находим индекс начала значения id
        if id_index != -1:
            obj_id = url[id_index + 3:]  # извлекаем значение id
        else:
            obj_id = 'N/A'

        response = session.get(full_url, headers=HEADERS)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            input_element = soup.find('input', {'type': 'image', 'src': 'https://dcdn.heroeswm.ru/i/getjob/btn_work.png', 'class': 'getjob_submitBtn', 'onclick': 'return obj_c(0);', 'id': 'wbtn'})
            if input_element:
                print(f"Кнопка есть {full_url}. ID: {obj_id}")
                post_data = {
                    "x": "1",
                    "y": "1",
                    "id": obj_id,
                    "id2": obj_id,
                    "idr": "ba98cdc1a668b8d54d55e546570b6b66",
                    "num": "0",
                    "work_code_data_element": "0",
                    "id3": "8cdce3392c6aa7b65d260bfc130b8c04",
                }
                post_response = session.post('https://www.heroeswm.ru/object_do.php', data=post_data, headers=HEADERS)
                return True  # Возвращаем True если кнопка найдена и нажата
            else:
                print(f"Кнопки нет {full_url}. ID: {obj_id}")
        else:
            print(f"Failed to retrieve {full_url}")

    return False  # Возвращаем False если кнопка не найдена
    
def_requests = s.get('https://www.heroeswm.ru/map.php?st=sh', headers=HEADERS)
soup = BeautifulSoup(def_requests.content, 'html.parser')
container = soup.find('div', {'id': 'hwm_map_objects_and_buttons'})
if container:
    resume_links = [link.get('href') for link in container.find_all('a', href=True) if 'object-info.php?id=' in link.get('href')]
    # Преобразование в set для удаления дубликатов и обратно в список
    unique_links = list(set(resume_links))
else:
    print("Контейнер не найден")

while True:
    result = ParseLinks(unique_links, s, HEADERS)  # Вызываем функцию и получаем результат
    if result:  # Если результат True
        print("Кнопка была нажата. Вызываем функцию через час.")
        random_time = random.randint(3600, 3900)  # Генерируем случайное число от 3600 до 3700
        time.sleep(random_time)  # Ждем 1 час перед повторным вызовом функции
    else:  # Если результат False
        print("Кнопка не была нажата. Вызываем функцию через 1 минуту.")
        random_time = random.randint(300, 360)  # Генерируем случайное число от 3600 до 3700
        time.sleep(random_time) # Ждем 1 минуту перед повторным вызовом функции