from lxml import html
import requests
from pymongo import MongoClient


client = MongoClient('127.0.0.1', 27017)
client.drop_database('lenta_news')
db = client.lenta_news
db.create_collection('lenta_news_list')
collection = db.lenta_news_list


class LentaRuParser:
    host = 'https://lenta.ru'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/94.0.4606.85 YaBrowser/21.11.1.932 Yowser/2.5 Safari/537.36'}

    def parse(self) -> list:
        news_list = []
        response = requests.get(self.host, headers=self.headers)
        dom = html.fromstring(response.text)
        news_elements = dom.xpath("//section[contains(@class,'js-top-seven')]//div[@class='item']")
        for element in news_elements:
            news = {
                'title': str(element.xpath("./a/text()")[0]),
                'url':  self.host + str(element.xpath("./a/@href")[0]),
                'source': 'LENTA_RU',
                'publication_date': str(element.xpath("./a/time/@datetime")[0])
            }
            news_list.append(news)
        return news_list


if __name__ == '__main__':
    parser = LentaRuParser()
    news_result = parser.parse()
    collection.insert_many(news_result)
