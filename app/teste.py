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

    # Encontrando o script que contém as informações
    script = soup.find('script', type='application/ld+json')

    site = extrair_url(url)
    name = ""
    price = ""

    # Verificando se encontrou o script com as informações
        # Buscando nome no meta
        meta_name = soup.find('meta', {'property': 'og:title'})
        if meta_name:
            name = meta_name['content']

    print("Site:", site)
    print("Nome:", name)
    print("Preço:", price)
