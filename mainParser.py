import requests
from bs4 import BeautifulSoup
import csv

CSV = cards.csv
HOST = "https://www.ozon.ru"
URL = "https://www.ozon.ru/category/elektrogitary-13926/?category_was_predicted=true&deny_category_prediction=true&from_global=true&text=электрогитара"
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 OPR/90.0.4480.100'
}

def get_html(url, params=''):
    html = requests.get(url, headers=HEADERS, params=params)
    return html


def get_content(html):
    soup = BeautifulSoup(html, "html.parser")
    items = soup.findAll("div", class_="catalog-product ui-button-widget ")
    cards = []

    for item in items: # Забираем информацию
        cards.append(
            {
                "title":item.find("div", class_="title").get_text(strip=True),
                "link_product": HOST + item.find("div", class_="title").get_text().find('a').get("href"),
                "brand":item.find("div", class_="title").get_text(strip=True),
                "card_image": HOST + item.find("div", class_="title").find("img").get("scr"),
            }
        )
    return cards

def parser():
    PAGENATION = input("Укажите кол-во страниц для парсинга: ")
    PAGENATION = int(PAGENATION.strip())

    html = get_html(URL)
    if html.status_code == 200:
        cards = []
        for page in range(1, PAGENATION):
            print(f'Парсим страницу: {page}')
            html = get_html(URL, params={"page": page})
            cards.extend(get_content(html.text))

        print(f"Парсинг закончил")
        print(cards)
    else:
        print("Eror")

    def save_doc(items, path):
        with open(path,  "w", newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(['Название продукта', 'Ссылка на продукт', "Банк", "Изображение"])
            for item in items:
                writer.writerow([item['title'], item['link_product'], item['brand'], item['card_image']])
                save_doc(cards, CSV)

parser()