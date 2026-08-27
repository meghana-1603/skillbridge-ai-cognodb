from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

load_dotenv()

URI = os.getenv("DB_URI")
USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")

driver = GraphDatabase.driver(
    URI,
    auth=(USER, PASSWORD)
)

def get_driver():
    return driver
