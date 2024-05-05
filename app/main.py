import requests
from bs4 import BeautifulSoup
import json
import re

# URL da página
urls = [
    "https://www.terabyteshop.com.br/produto/28528/placa-de-video-msi-nvidia-geforce-rtx-4070-super-ventus-3x-oc-12gb-gddr6x-dlss-ray-tracing-912-v513-643",
    "https://www.kabum.com.br/produto/520534/placa-de-video-rtx-4070-super-msi-12g-ventus-3x-oc-nvidia-geforce-12gb-gddr6x-dlss-ray-tracing",
]

# Definir uma função para extrair a informação entre "www." e ".com" usando regex
def extract_info(url):
    match = re.search(r'www\.(.*?)\.com', url)
    if match:
        return match.group(1)
    else:
        return None

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

for url in urls:
    # Fazendo o request para a página
   response = requests.get(url, headers=headers)
   soup = BeautifulSoup(response.text, 'html.parser')
   
   # Encontrando o script que contém as informações
   script = soup.find('script', type='application/ld+json')
   data = json.loads(script.string)
   
   # Extraindo o valor do preço
   company = extract_info(url)
   price = data['offers']['price']
   name = data['name']

   print("Empresa:", company)
   print("Nome:", name)
   print("Preço:", price)
   