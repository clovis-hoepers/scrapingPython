import requests
from bs4 import BeautifulSoup
import json
import re
import os
import pandas as pd

# Caminho do arquivo TXT
diretorio_atual = os.getcwd()
caminho_arquivo = os.path.join(diretorio_atual, 'app/urls.txt')

# Carregar o conteúdo do arquivo em um DataFrame do Pandas
df = pd.read_csv(caminho_arquivo, header=None, names=['URL'])

# Extrair as URLs como uma lista
urls = df['URL'].tolist()

# Definir uma função para extrair a informação entre "www." e ".com" usando regex


def extrair_url(url):
    padrao = re.compile(r'https?://(.*?)/')
    resultado = padrao.search(url)
    if resultado:
        return resultado.group(1)
    else:
        return None


headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
}

for url in urls:
    # Fazendo o request para a página
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Erro ao fazer o request para a página:", url)
        continue
    soup = BeautifulSoup(response.text, 'html.parser')

    site = extrair_url(url)
    name = None
    price = None

    # Procurando todas as metatags relevantes
    for meta_tag in soup.find_all('meta'):
        if 'property' in meta_tag.attrs and 'content' in meta_tag.attrs:
            if 'og:title' in meta_tag['property']:
                name = meta_tag['content']
            elif 'product:price:amount' in meta_tag['property']:
                price = meta_tag['content']

    # Se o nome ou o preço ainda estiverem vazios, tenta encontrar na página HTML
    if hasattr(soup.find('script', type='application/ld+json', string=re.compile(r'"@type": "Product"')), 'string'):
        script = soup.find('script', type='application/ld+json',
                           string=re.compile(r'"@type": "Product"'))
        script_data = json.loads(script.string)
        name = script_data['name']

    if not name and hasattr(soup.find('script', type='application/ld+json', string=re.compile(r'"name":')), 'string'):
        script = soup.find(
            'script', type='application/ld+json', string=re.compile(r'"name":'))
        script_data = json.loads(script.string)
        name = script_data['name']
    
    if not name and hasattr(soup.find('script', string=re.compile(r'"priceSell":')), 'string'):
        name = soup.find('h1')

    if hasattr(soup.find('span', class_='preco'), 'string'):
        price_tag = soup.find('span', class_='preco')
        price = price_tag.text.strip()

    if price is None and hasattr(soup.find('script', string=re.compile(r'"priceSell":')), 'string'):
        price_tag = soup.find('script', string=re.compile(r'"priceSell":'))
        price_tag = (price_tag.string)
        price_tag = price_tag.replace('dataLayer = ', '')
        price_tag = json.loads(price_tag)
        price = price_tag[0]['priceSell']

    if price is None and hasattr(soup.find('script', type='application/ld+json', string=re.compile(r'"price":')), 'string'):
        script = soup.find('script', type='application/ld+json',
                           string=re.compile(r'"price":'))
        script_data = json.loads(script.string)
        price = script_data['offers']['price']

    if price is None and hasattr(soup.find('script', type='application/ld+json', string=re.compile(r'"@type": "Product"')), 'string'):
        script = soup.find('script', type='application/ld+json',
                           string=re.compile(r'"@type": "Product"'))
        script_data = json.loads(script.string)
        name = script_data['price']

    print("Site:", site)
    print("Nome:", name)
    print("Preço:", price)
