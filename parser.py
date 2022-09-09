import requests
from bs4 import BeautifulSoup

url = 'https://www.banki.ru/products/currency/cb/'

source = requests.get(url)
main_text = source.text
soup = BeautifulSoup(main_text)

tr = soup.find('tr', {'data-currency-code': 'USD'}).text

dollarExchangeRate = tr[34:]

dollarExchangeRate = dollarExchangeRate[:7]


print("Курс доллара: " + dollarExchangeRate + ' рублей')
