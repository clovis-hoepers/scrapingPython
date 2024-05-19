import time
from datetime import datetime
import logging
from utils.web_scraping import extract_data
from utils.mysql_operations import insert_to_mysql, create_database_table
from models.download_operations import download_file
from models.data_operations import load_urls_from_file

# Configurando o sistema de log para imprimir na saída padrão
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == "__main__":
    while True:
        try:
            urls_file_url = "https://drive.google.com/uc?id=1LA5Bt99eSLk5n8g2FmXiHN-jfDyKTwIT"
            output_path = "urls.txt"
            download_file(urls_file_url, output_path)

            urls = load_urls_from_file(output_path)

            if create_database_table():
                logging.info(
                    "Base de dados e tabela criadas com sucesso ou já existentes.")
            else:
                logging.error(
                    "Falha ao criar a base de dados ou tabela. Verifique os logs para detalhes.")

            for url in urls:
                try:
                    site, name, price = extract_data(url)
                    if site and name and price:
                        insert_to_mysql(site, name, price, url)
                except Exception as e:
                    logging.error(f"Erro ao processar URL: {
                                  url}. Detalhes: {e}")

            logging.info("Executado em: %s",
                         datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            time.sleep(1800)  # Aguarda 30 minutos antes de recomeçar o ciclo
        except Exception as e:
            logging.error(f"Erro durante a execução: {e}")
