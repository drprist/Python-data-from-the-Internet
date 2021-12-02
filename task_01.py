import requests
from bs4 import BeautifulSoup
from pprint import pprint
import re
import pandas as pd
from pymongo import MongoClient

# Раскомментировать для первого использования
# pip install pymongo
# client.drop_database('hh')
# db.create_collection('hh_list')

client = MongoClient('127.0.0.1', 27017)
db = client.hh
collection = db.hh_list

page = 0
double = 0
vacant_list = []

while page < 100:
    url = 'https://hh.ru'
    params = {'search_field': ['name', 'company_name', 'description'],
              'fromSearchLine': 'true',
              'text': 'python',  # Текст запроса к поиску
              'page': page,
              'items_on_page': 20}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/94.0.4606.85 YaBrowser/21.11.1.932 Yowser/2.5 Safari/537.36'}
    response = requests.get(url + '/search/vacancy', params=params, headers=headers)
    dom = BeautifulSoup(response.text, 'html.parser')
    vacancies = dom.find_all('div', {'class', 'vacancy-serp-item'})
    for vacant in vacancies:
        vacant_data = {}
        name = vacant.find('a', {'class': 'bloko-link'})
        link = name.get('href')
        name = name.text
        try:
            coast = vacant.find('div', {'class': 'vacancy-serp-item__sidebar'}).text
            coast_split = coast.split()
            coast_join = "".join(coast_split)
            replaced_coast = re.sub('[\D]', ' ', coast_join)
            replaced_coast_split = replaced_coast.split()
            if len(replaced_coast_split) > 1:
                min_coast = int(replaced_coast_split[0])
                max_coast = int(replaced_coast_split[1])
            else:
                min_coast = int(replaced_coast_split[0])
                max_coast = None
            currency = coast_split[-1]
        except:
            min_coast = None
            max_coast = None
            currency = None

        vacant_data['name'] = name
        vacant_data['min_coast'] = min_coast
        vacant_data['max_coast'] = max_coast
        vacant_data['currency'] = currency
        vacant_data['link'] = link
        vacant_data['url'] = url

        def unique_vacant(v, d):  # Функция, которая добавляет только новые вакансии в базу
            vac_link = v['link']
            if collection.count_documents({'link': vac_link}) > 0:
                d += 1
            else:
                vacant_list.append(vacant_data)

        unique_vacant(vacant_data, double)

    pprint(F"Всего получено {len(vacant_list)} новых вакансий, просмотрено {page + 1} страниц")
    page += 1

df = pd.DataFrame(vacant_list)
df.to_csv('task_01.csv', encoding="utf-8-sig")
collection.insert_many(vacant_list)
