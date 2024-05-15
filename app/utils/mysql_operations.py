import os
from datetime import datetime
import logging
import mysql.connector
from mysql.connector import errorcode
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    site = Column(String(255))
    name = Column(String(255))
    price = Column(Float)
    datetime_inserted = Column(DateTime, default=datetime.now)


# Configurando o sistema de log para imprimir na saída padrão se não puder criar o arquivo de log
log_file = 'database.log'
try:
    # Tenta criar o arquivo de log
    open(log_file, 'a').close()
except Exception as e:
    # Se não puder criar o arquivo de log, imprime uma mensagem de erro
    print(f"Erro ao criar arquivo de log: {e}")
    # Define log_file como None para usar a saída padrão
    log_file = None

if log_file:
    # Se o arquivo de log foi criado com sucesso, configure o logger para usá-lo
    logging.basicConfig(filename=log_file, level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
else:
    # Se não foi possível criar o arquivo de log, configure o logger para imprimir na saída padrão
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')


def create_database_table():
    try:
        # Conectar ao MySQL para criar a tabela
        cnx = mysql.connector.connect(user=os.getenv('MYSQL_USER', 'admin'),
                                      password=os.getenv(
                                          'MYSQL_PASSWORD', 'admin'),
                                      host=os.getenv(
                                          'MYSQL_HOST', 'localhost'),
                                      port=os.getenv('MYSQL_PORT', '3306'),
                                      database=os.getenv('MYSQL_DATABASE', 'database_products'))
        cursor = cnx.cursor()

        # Criar tabela se não existir
        create_table_query = '''
            CREATE TABLE IF NOT EXISTS products (
                id INT AUTO_INCREMENT PRIMARY KEY,
                site VARCHAR(255),
                name VARCHAR(255),
                price FLOAT,
                datetime_inserted DATETIME
            )
        '''
        cursor.execute(create_table_query)
        cnx.commit()

        cursor.close()
        cnx.close()

        logging.info("Tabela 'products' criada com sucesso ou já existente.")
        return True
    except mysql.connector.Error as e:
        if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            logging.error(
                "Erro de acesso ao MySQL: Usuário ou senha incorretos")
        elif e.errno == errorcode.ER_BAD_DB_ERROR:
            logging.error("Erro de acesso ao MySQL: Banco de dados não existe")
        else:
            logging.error(f"Erro ao criar a tabela 'products'. Detalhes: {e}")
        return False


def insert_to_mysql(site, name, price, url):
    try:
        # Verifica se o preço é uma string e tenta converter para float
        if isinstance(price, str):
            price = float(price)

        # Arredonda o preço para duas casas decimais
        price = round(price, 2)

        # Conectar ao MySQL para inserir dados
        cnx = mysql.connector.connect(user=os.getenv('MYSQL_USER', 'admin'),
                                      password=os.getenv(
                                          'MYSQL_PASSWORD', 'admin'),
                                      host=os.getenv(
                                          'MYSQL_HOST', 'localhost'),
                                      port=os.getenv('MYSQL_PORT', '3306'),
                                      database=os.getenv('MYSQL_DATABASE', 'database_products'))
        cursor = cnx.cursor()

        # Inserir dados
        insert_query = '''
            INSERT INTO products (site, name, price, datetime_inserted)
            VALUES (%s, %s, %s, %s)
        '''
        data = (site, name, price, datetime.now())
        cursor.execute(insert_query, data)
        cnx.commit()

        cursor.close()
        cnx.close()

        logging.info(
            "Dados inseridos no MySQL: site=%s, name=%s, price=%s", site, name, price)
    except mysql.connector.Error as e:
        logging.error(
            "Erro ao inserir dados no MySQL para a URL %s. Detalhes: %s", url, e)

# Criar a tabela 'products' explicitamente
create_database_table()
