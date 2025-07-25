from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

if not all([DB_HOST, DB_NAME, DB_USER, DB_PASS]):
    raise ValueError("Configuração do banco de dados incompleta. Verifique as variáveis de ambiente.")