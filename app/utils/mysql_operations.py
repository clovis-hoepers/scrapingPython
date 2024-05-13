import mysql.connector

mysql_username = "admin"
mysql_password = "admin"
mysql_host = "mysql"
mysql_port = 3306
mysql_database = "database_products"
mysql_table = "products"


def create_database_table():
    try:
        connection = mysql.connector.connect(
            host=mysql_host,
            user=mysql_username,
            password=mysql_password,
            port=mysql_port
        )

        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {mysql_database}")
        print("Database criada com sucesso ou já existente.")

        cursor.execute(f"USE {mysql_database}")
        print("Usando a base de dados:", mysql_database)

        cursor.execute(f"CREATE TABLE IF NOT EXISTS {
                       mysql_table} (id INT AUTO_INCREMENT PRIMARY KEY, site VARCHAR(255), name VARCHAR(255), price FLOAT, datetime_inserted DATETIME)")
        print("Tabela criada com sucesso ou já existente.")

        connection.commit()
        cursor.close()
        connection.close()
        return True
    except mysql.connector.Error as error:
        print("Erro ao conectar ao servidor MySQL:", error)
        return False


def insert_to_mysql(site, name, price):
    try:
        connection = mysql.connector.connect(
            host=mysql_host,
            user=mysql_username,
            password=mysql_password,
            port=mysql_port,
            database=mysql_database
        )

        cursor = connection.cursor()
        sql_query = f"INSERT INTO {
            mysql_table} (site, name, price, datetime_inserted) VALUES (%s, %s, %s, %s)"
        data = (site, name, str(price),
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        cursor.execute(sql_query, data)
        connection.commit()
        print("Dados inseridos no MySQL:", data)
    except mysql.connector.Error as error:
        print("Erro ao inserir dados no MySQL:", error)
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
