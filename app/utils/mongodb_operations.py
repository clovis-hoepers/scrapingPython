from pymongo import MongoClient
from datetime import datetime

mongo_username = "admin"
mongo_password = "admin" #sim, coloque uma senha forte, a mesma do docker-compose

client = MongoClient(
    "mongodb://%s:%s@mongodb:27017/" % (mongo_username, mongo_password)
)
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
