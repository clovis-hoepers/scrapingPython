import time
from datetime import datetime

from utils.web_scraping import extract_data
from utils.mysql_operations import insert_to_mysql
from models.download_operations import download_file
from models.data_operations import load_urls_from_file


while True:
    # URL do seu arquivo, lembre de alterar a permissao para publico
    urls_file_url = "https://drive.google.com/uc?id=1LA5Bt99eSLk5n8g2FmXiHN-jfDyKTwIT"
    output_path = "urls.txt"
    download_file(urls_file_url, output_path)

    urls = load_urls_from_file(output_path)

    for url in urls:
        site, name, price = extract_data(url)
        if site and name and price:
            insert_to_mysql(site, name, price)

    print("Executado em:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    time.sleep(1800)
