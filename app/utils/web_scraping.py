import json
import re
import logging
from models.price_formatting import format_price
import urllib.request
from bs4 import BeautifulSoup

def extract_data(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
        }
        
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            html = response.read()
            
        soup = BeautifulSoup(html, 'html.parser')

        site = extract_site(url)
        name, price = extract_name_and_price(soup)

        return site, name, price
    
    except Exception as e:
        logging.error("Erro ao extrair dados da página: %s", e)
        return None, None, None

def extract_site(url):
    try:
        pattern = re.compile(r'https?://(.*?)/')
        result = pattern.search(url)
        return result.group(1) if result else None
    except Exception as e:
        logging.error("Erro ao extrair o site da URL: %s", e)
        return None

def extract_name_and_price(soup):
    name = None
    price = None

    # Lista de padrões para buscar nome e preço
    patterns = [
        ('og:title', 'content'),
        ('product:price:amount', 'content'),
        ('application/ld+json', 'name'),
        ('application/ld+json', 'price'),
        ('h1', None),
        ('span', 'preco')
    ]

    for pattern, attribute in patterns:
        try:
            if attribute:
                tag = soup.find(property=pattern)
                if tag:
                    if attribute == 'content':
                        value = tag.get(attribute)
                    elif attribute == 'name':
                        value = json.loads(tag.string)['name']
                    elif attribute == 'price':
                        value = format_price(json.loads(tag.string)['price'])
                    else:
                        value = tag.text.strip()
            else:
                tag = soup.find(pattern)
                value = tag.text.strip() if tag else None

            if value:
                if 'price' in pattern:
                    price = value
                else:
                    name = value

            if name and price:
                break

        except Exception as e:
            logging.error("Erro ao extrair dados usando padrão %s: %s", pattern, e)

    return name, price
