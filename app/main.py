import requests
from bs4 import BeautifulSoup
import json
import re

# URLs da página
urls = [
    "https://www.pichau.com.br/placa-de-video-msi-geforce-rtx-4070-super-ventus-3x-oc-12gb-gddr6x-192-bit-912-v513-643",
    "https://www.terabyteshop.com.br/produto/28528/placa-de-video-msi-nvidia-geforce-rtx-4070-super-ventus-3x-oc-12gb-gddr6x-dlss-ray-tracing-912-v513-643",
    "https://www.kabum.com.br/produto/520534/placa-de-video-rtx-4070-super-msi-12g-ventus-3x-oc-nvidia-geforce-12gb-gddr6x-dlss-ray-tracing",
    "https://www.bioageprofissional.com.br/protocolo-limpeza-de-pele-bio-clean-system",
    "https://www.lojaadcos.com.br/protetor-solar-tonalizante-fps50-pocompacto-acido-hialuronico/p",
    "https://www.ellementtistore.com.br/produto/espuma-hydra-repair-gest-care/4928107",
    "https://www.tulipia.com.br/floraty-creme-emoliente-cravos/p",
    "https://www.lakma.com.br/home-care/mascara-clareadora-10g",
    "https://www.extratosdaterra.com.br/fotoprotetor-facial-fps-30---50-g/p"
]

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
    soup = BeautifulSoup(response.text, 'html.parser')

    site = extrair_url(url)
    name = ""
    price = ""

    # Procurando todas as metatags relevantes
    for meta_tag in soup.find_all('meta'):
        if 'property' in meta_tag.attrs and 'content' in meta_tag.attrs:
            if 'og:title' in meta_tag['property']:
                name = meta_tag['content']
            elif 'product:price:amount' in meta_tag['property']:
                price = meta_tag['content']

    # Se o nome ou o preço ainda estiverem vazios, tenta encontrar no script JSON-LD
    if not name or not price:
        script = soup.find('script', type='application/ld+json')
        if script and hasattr(script, 'string'):
            script_data = json.loads(script.string)
            if not name:
                name = script_data.get('name', '')
            if not price and 'offers' in script_data:
                price = script_data['offers'].get('price', '')

    # Se o nome ou o preço ainda estiverem vazios, tenta encontrar na página HTML
    if not name or not price:
        name_tag = soup.find('h1')
        if name_tag:
            name = name_tag.text.strip()

        price_tag = soup.find('span', class_='price')
        if price_tag:
            price = price_tag.text.strip()

    print("Site:", site)
    print("Nome:", name)
    print("Preço:", price)
