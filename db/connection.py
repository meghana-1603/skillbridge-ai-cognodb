from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

load_dotenv()

try:
    import streamlit as st
    URI = st.secrets["DB_URI"]
    USER = st.secrets["DB_USER"]
    PASSWORD = st.secrets["DB_PASSWORD"]
except Exception:
    URI = os.getenv("DB_URI")
    USER = os.getenv("DB_USER")
    PASSWORD = os.getenv("DB_PASSWORD")

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

def get_driver():
    return driver
