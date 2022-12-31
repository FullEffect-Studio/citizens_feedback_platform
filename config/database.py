# config/database.py
from pymongo import MongoClient

client = MongoClient("mongodb+srv://admin:fulleffect@cluster0.b7xsp.mongodb.net/buspro_dev?retryWrites=true&w=majority")
db = client["buspro_dev"]
