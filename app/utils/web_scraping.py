import requests
from bs4 import BeautifulSoup
import json
import re
from models.price_formatting import format_price


def extract_data(url):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Erro ao fazer o request para a página:", url)
        return None, None, None
    soup = BeautifulSoup(response.text, 'html.parser')

    site = extract_site(url)
    name, price = extract_name_and_price(soup)

    return site, name, price


def extract_site(url):
    pattern = re.compile(r'https?://(.*?)/')
    result = pattern.search(url)
    if result:
        return result.group(1)
    else:
        return None


def extract_name_and_price(soup):
    name = None
    price = None
#Existem N formas de extrair o nome e o preco de um site, depende da modelagem, insira aqui as outras formas que desejar
    for meta_tag in soup.find_all('meta'):
        if 'property' in meta_tag.attrs and 'content' in meta_tag.attrs:
            if 'og:title' in meta_tag['property']:
                name = meta_tag['content']
            elif 'product:price:amount' in meta_tag['property']:
                price = format_price(meta_tag['content'])

    if hasattr(soup.find('script', type='application/ld+json', string=re.compile(r'"@type": "Product"')), 'string'):
        script = soup.find('script', type='application/ld+json',
                           string=re.compile(r'"@type": "Product"'))
        script_data = json.loads(script.string)
        name = script_data['name']

    if not name and hasattr(soup.find('script', type='application/ld+json', string=re.compile(r'"name":')), 'string'):
        script = soup.find('script', type='application/ld+json',
                           string=re.compile(r'"name":'))
        script_data = json.loads(script.string)
        name = script_data['name']

    if not name and hasattr(soup.find('script', string=re.compile(r'"priceSell":')), 'string'):
        name = soup.find('h1')

    if hasattr(soup.find('span', class_='preco'), 'string'):
        price_tag = soup.find('span', class_='preco')
        price = format_price(price_tag.text.strip())

    if price is None and hasattr(soup.find('script', string=re.compile(r'"priceSell":')), 'string'):
        price_tag = soup.find('script', string=re.compile(r'"priceSell":'))
        price_tag = (price_tag.string)
        price_tag = price_tag.replace('dataLayer = ', '')
        price_tag = json.loads(price_tag)
        price = format_price(price_tag[0]['priceSell'])

    if price is None and hasattr(soup.find('script', type='application/ld+json', string=re.compile(r'"price":')), 'string'):
        script = soup.find('script', type='application/ld+json',
                           string=re.compile(r'"price":'))
        script_data = json.loads(script.string)
        price = format_price(script_data['offers']['price'])

    if price is None and hasattr(soup.find('script', type='application/ld+json', string=re.compile(r'"@type": "Product"')), 'string'):
        script = soup.find('script', type='application/ld+json',
                           string=re.compile(r'"@type": "Product"'))
        script_data = json.loads(script.string)
        price = format_price(script_data['price'])

    return name, price
