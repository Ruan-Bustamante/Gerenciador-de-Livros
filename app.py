from flask import Flask, request, jsonify
import psycopg2
from psycopg2 import extras  # Importing extras for dictionary RealDictCursor

app = Flask(__name__)

# Configurações do Banco de Dados

DB_HOST = 'localhost' # Endereço do servidor PostgreSQL
DB_NAME = 'gerenciador_livros_db' # Nome do banco de dados
DB_USER = 'gerenciador_livros_admin' # Usuário do banco de dados
DB_PASS = '123456' # Senha do usuário do banco de dados

def get_db_connection():
    # Função para conectar ao banco de dados

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

# Garante que o banco de dados esteja inicializado

with app.app_context():
    init_db()

# Rotas API

@app.route('/livros', methods=['GET'])
def get_livros():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
    cursor.execute('SELECT * FROM livros;')
    livros = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(livros)

@app.route('/livros', methods=['POST'])
def add_livro():
    novo_livro = request.get_json()
    titulo = novo_livro['titulo']
    autor = novo_livro['autor']
    ano_publicacao = novo_livro.get('ano_publicacao')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO livros (titulo, autor, ano_publicacao)
        VALUES (%s, %s, %s) RETURNING id;
    ''', (titulo, autor, ano_publicacao))
    livro_id = cursor.fetchone()[0]  # Pega o ID do livro recém-criado
    conn.commit()
    cursor.close()
    conn.close()

    # Retorna o livro criado com o ID gerado pelo banco de dados

    return jsonify({"id": livro_id, "titulo": titulo, "autor": autor, "ano_publicacao": ano_publicacao}), 201 # 201 = Created

@app.route('/livros/<int:livro_id>', methods=['GET'])
def get_livro(livro_id):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
    cursor.execute('SELECT * FROM livros WHERE id = %s;', (livro_id,))
    livro = cursor.fetchone()  # Pega apenas um resultado
    cursor.close()
    conn.close()

    if livro is None:
        return jsonify({"error": "Livro não encontrado"}), 404
    return jsonify(livro)

@app.route('/livros/<int:livro_id>', methods=['PUT'])
def update_livro(livro_id):
    dados_atualizados = request.get_json()
    titulo = dados_atualizados.get('titulo')
    autor = dados_atualizados.get('autor')
    ano_publicacao = dados_atualizados.get('ano_publicacao')

    conn = get_db_connection()
    cursor = conn.cursor()

    # Monta a query de atualização dinamicamente (somente campos fornecidos)

    update_fields = []
    update_values = []
    if titulo:
        update_fields.append("titulo = %s")
        update_values.append(titulo)
    if autor:
        update_fields.append("autor = %s")
        update_values.append(autor)
    if ano_publicacao is not None:
        update_fields.append("ano_publicacao = %s")
        update_values.append(ano_publicacao)
    
    if not update_fields:  # Se nenhum campo for fornecido, retorna erro
        return jsonify({"error": "Nenhum campo para atualizar"}), 400

    query = f"UPDATE livros SET {', '.join(update_fields)} WHERE id = %s RETURNING *;"
    update_values.append(livro_id)

    cursor.execute(query, tuple(update_values))
    livro_atualizado = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()

    if livro_atualizado is None:
        return jsonify({"error": "Livro não encontrado"}), 404
    
    # Busca o livro atualizado para retornar como JSON
    conn_fetch = get_db_connection()
    cursor_fetch = conn_fetch.cursor(cursor_factory=extras.RealDictCursor)
    cursor_fetch.execute('SELECT * FROM livros WHERE id = %s;', (livro_id,))
    livro_retornado = cursor_fetch.fetchone()
    cursor_fetch.close()
    conn_fetch.close()

    return jsonify(livro_retornado)

@app.route('/livros/<int:livro_id>', methods=['DELETE'])
def delete_livro(livro_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM livros WHERE id = %s RETURNING *;', (livro_id,))
    livro_deletado = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()

    if livro_deletado is None:
        return jsonify({"error": "Livro não encontrado"}), 404
    
    return jsonify({"message": "Livro deletado com sucesso", "livro": livro_deletado})

# Executa a aplicação

if __name__ == '__main__':
    app.run(debug=True) # debug=True para desenvolvimento, desative em produção