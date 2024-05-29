# -*- config: utf-8 -*-
import requests
from selenium import webdriver
import bs4
from time import sleep
import csv
from datetime import datetime


def parser() -> dict:
    """Парсит сайт coinmarketcap.com. Берет данные(наименование, капитализация) первых 100 криптовалют"""
    driver = webdriver.Chrome()
    driver.get('https://coinmarketcap.com/')
    driver.maximize_window()
    px = 0  # эта часть кода отвечает за получения кода с сайта, на выходе остается
    # обычный файл супа с которым можно работать
    for i in range(10):
        px += 1000
        driver.execute_script(f'window.scrollTo(0, {px})')
        sleep(0.1)

    html = driver.page_source
    driver.close()
    soup = bs4.BeautifulSoup(html, 'html.parser')
    # Извлекается таблица с данными о криптовалютах
    table = soup.find('tbody').find_all('tr')
    name_capitalization = {}
    for tr in table:
        try:
            # Извлекаются все ячейки (<td>)
            all_td = list(tr.find_all('td'))
            # Извлекается наименование криптовалюты из второй ячейки
            name = all_td[2]
            name = name.find_all('p')[0].get_text()
            # Извлекается капитализация из восьмой ячейки
            capitalization = all_td[7]
            capitalization = capitalization.find_all('span')[1].get_text()
            # Данные добавляются в словарь name_capitalization
            name_capitalization[name] = capitalization.replace('$', '').replace(',', '')
        except IndexError as e:
            print(e)
    return name_capitalization


def write_cmc_top(nac, name_cripto):
    cripto_value = []
    try:
        # Получаю данные из словаря, которые вернула функция parser
        cripto_capitalization = int(nac[name_cripto])
        total_sum_capitalization = sum(int(value) for value in nac.values())
        percent = cripto_capitalization / total_sum_capitalization * 100
        # Добаваляю эти данные и отформатированное текущее время в список
        cripto_value.append(name_cripto)
        cripto_value.append(total_sum_capitalization)
        cripto_value.append(f'{percent}%')
        now = datetime.now()
        formatted_time = now.strftime("%H.%M %d.%m.%Y")
        cripto_value.append(formatted_time)
        return cripto_value
    except KeyError as e:
        print(e)


# Создаю новый файл с названием, сформированным из текущего времени
cripto_title = ['Name', 'MC', 'MP']

name_and_capitalization = parser()
c_v = write_cmc_top(name_and_capitalization, name_cripto='USDC')
file_name = c_v[3]
with open(file_name, 'a', newline='') as some_file:
    writer = csv.writer(some_file, delimiter=' ')
    writer.writerow(cripto_title)
    writer.writerow(c_v[:3])
