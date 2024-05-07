from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb://localhost:27017/")
db = client["database_products"]
collection = db["products"]

def insert_to_mongodb(site, name, price):
    data = {
        "site": site,
        "name": name,
        "price": price,
        "datetime_inserted": datetime.now()
    }
    collection.insert_one(data)
    print("Dados inseridos no MongoDB:", data)