import os
from datetime import datetime
import logging
import mysql.connector
from mysql.connector import errorcode
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    site = Column(String(255))
    name = Column(String(255))
    price = Column(Float)
    datetime_inserted = Column(DateTime, default=datetime.now)


log_file = 'database.log'
try:
    open(log_file, 'a').close()
except Exception as e:
    print(f"Erro ao criar arquivo de log: {e}")
    log_file = None

if log_file:
    logging.basicConfig(filename=log_file, level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
else:
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')


def create_database_table():
    try:
        engine = create_engine(get_mysql_connection_string())
        Base.metadata.create_all(engine)
        logging.info("Tabela 'products' criada com sucesso ou já existente.")
        return True
    except Exception as e:
        logging.error(f"Erro ao criar a tabela 'products'. Detalhes: {e}")
        return False


def get_mysql_connection_string():
    return f"mysql+mysqlconnector://{os.getenv('MYSQL_USER', 'admin')}:{os.getenv('MYSQL_PASSWORD', 'admin')}@mysql:{os.getenv('MYSQL_PORT', '3306')}/{os.getenv('MYSQL_DATABASE', 'database_products')}"

def insert_to_mysql(site, name, price, url):
    try:
        if isinstance(price, str):
            price = float(price)
        price = round(price, 2)

        # Use mysql-connector-python para conexão
        cnx = mysql.connector.connect(
            user=os.getenv('MYSQL_USER', 'admin'),
            password=os.getenv('MYSQL_PASSWORD', 'admin'),
            host=os.getenv('MYSQL_HOST', 'localhost'),
            port=os.getenv('MYSQL_PORT', '3306'),
            database=os.getenv('MYSQL_DATABASE', 'database_products'),
            allow_public_key_retrieval=True  # Permite recuperação de chave pública
        )

        cursor = cnx.cursor()
        add_product = ("INSERT INTO products "
                       "(site, name, price) "
                       "VALUES (%s, %s, %s)")
        data_product = (site, name, price)
        cursor.execute(add_product, data_product)
        cnx.commit()
        cursor.close()
        cnx.close()

        logging.info(
            "Dados inseridos no MySQL: site=%s, name=%s, price=%s", site, name, price)
    except Exception as e:
        logging.error(
            "Erro ao inserir dados no MySQL para a URL %s. Detalhes: %s", url, e)


create_database_table()
