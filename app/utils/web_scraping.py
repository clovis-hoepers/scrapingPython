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

    # Procurando pelo nome em diferentes padrões
    for meta_tag in soup.find_all('meta'):
        if 'property' in meta_tag.attrs and 'content' in meta_tag.attrs:
            if 'og:title' in meta_tag['property']:
                name = meta_tag['content']

    if not name:
        script = soup.find('script', type='application/ld+json',
                           string=re.compile(r'"@type": "Product"'))
        if script and 'name' in script.string:
            name = json.loads(script.string)['name']

    if not name:
        h1_tag = soup.find('h1')
        if h1_tag:
            name = h1_tag.text.strip()

    # Procurando pelo preço em diferentes padrões
    price_patterns = [
        ('product:price:amount', 'content'),
        ('application/ld+json', 'price'),
        ('span', 'preco')
    ]

    for pattern, attribute in price_patterns:
        try:
            if attribute:
                if pattern == 'application/ld+json':
                    script = soup.find('script', type=pattern,
                                       string=re.compile(r'"@type": "Product"'))
                    if script and 'offers' in script.string:
                        price = format_price(json.loads(
                            script.string)['offers']['price'])
                else:
                    tag = soup.find(pattern, class_=attribute)
                    if tag:
                        if attribute == 'content':
                            price = tag.get(attribute)
                        elif attribute == 'preco':
                            price = format_price(tag.text.strip())
                        else:
                            price = tag.text.strip()
            else:
                tag = soup.find(pattern)
                price = tag.text.strip() if tag else None

            if price:
                break

        except Exception as e:
            logging.error(
                "Erro ao extrair preço usando padrão %s: %s", pattern, e)

    return name, price
