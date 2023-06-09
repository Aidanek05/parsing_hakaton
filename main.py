from datetime import datetime

import json
import requests
from bs4 import BeautifulSoup, Tag

today = datetime.today().date()

URL = f'https://kaktus.media/?lable=8&date={today}&order=time'

def get_html(url: str) -> str:
    html = requests.get(url)
    return html.text

def cards_from_html(html: str):
    soup = BeautifulSoup(html, 'html.parser')
    cards = soup.find_all('div', class_ = 'Tag--article')
    return cards

def parse_data(cards):
    card: Tag
    news = []
    for card in cards:
        news_link = card.find('a', class_ = 'ArticleItem--image').get('href')
        new = {'title'  : card.find('a', class_ = 'ArticleItem--name').text.strip('\n'),
        'photo' : card.find('img', class_ = 'ArticleItem--image-img').get('src'),
        'news_link': news_link}
        news.append(new)
    return news

def get_description(news_link: str) -> str:
    html = get_html(news_link)
    soup = BeautifulSoup(html, 'html.parser')
    return soup.find('div', class_ = 'BbCode').find('p').text
        
def write_to_json(news):
    with open(f'news_{today}.json', 'w') as file:
        json.dump(news, file, indent=4, ensure_ascii=False)


def main():
    html = get_html(URL)
    cards = cards_from_html(html)
    news = parse_data(cards)
    write_to_json(news)

if __name__ == '__main__':
    main()