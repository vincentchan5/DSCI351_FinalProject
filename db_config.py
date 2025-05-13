import pymysql
from pymongo import MongoClient

# MySQL connection
def get_mysql_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='your_mysql_password',
        database='chatdb'
    )

# MongoDB connection
def get_mongo_connection():
    client = MongoClient('mongodb://localhost:27017/')
    return client['chatdb']  # Replace with your MongoDB DB name
