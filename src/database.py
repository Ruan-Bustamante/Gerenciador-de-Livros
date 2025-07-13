import psycopg2
from psycopg2 import extras
from config import DB_HOST, DB_NAME, DB_USER, DB_PASS # Importa as configurações do banco de dados

# Função para conectar ao banco de dados
def get_db_connection():
    
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    return conn



# Função para inicializar o esquema do banco de dados

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS livros (
            id SERIAL PRIMARY KEY,
            titulo VARCHAR(255) NOT NULL,
            autor VARCHAR(255) NOT NULL,
            ano_publicacao INT NULL
        );
    ''')
    conn.commit()
    cursor.close()
    conn.close()