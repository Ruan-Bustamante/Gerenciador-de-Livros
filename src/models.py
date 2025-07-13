from src.database import get_db_connection
from psycopg2 import extras  # Importando extras para usar RealDictCursor

def get_all_livros_db():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
    cursor.execute('SELECT * FROM livros;')
    livros = cursor.fetchall()
    cursor.close()
    conn.close()
    return livros

def add_livro_db(titulo, autor, ano_publicacao):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO livros (titulo, autor, ano_publicacao)
        VALUES (%s, %s, %s) RETURNING id;
    ''', (titulo, autor, ano_publicacao))
    livro_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return {"id": livro_id, "titulo": titulo, "autor": autor, "ano_publicacao": ano_publicacao}

def get_livro_by_id_db(livro_id):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
    cursor.execute('SELECT * FROM livros WHERE id = %s;', (livro_id,))
    livro = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if livro is None:
        return None
    return livro

def update_livro_db(livro_id, dados_atualizados):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    update_fields = []
    update_values = []
    
    if 'titulo' in dados_atualizados and dados_atualizados['titulo'] is not None:
        update_fields.append("titulo = %s")
        update_values.append(dados_atualizados['titulo'])
    if 'autor' in dados_atualizados and dados_atualizados['autor'] is not None:
        update_fields.append("autor = %s")
        update_values.append(dados_atualizados['autor'])
    if 'ano_publicacao' in dados_atualizados and dados_atualizados['ano_publicacao'] is not None:
        update_fields.append("ano_publicacao = %s")
        update_values.append(dados_atualizados['ano_publicacao'])

    if not update_fields:
        conn.close()
        return None # Indica que não há campos válidos para atualização

    query = f"UPDATE livros SET {', '.join(update_fields)} WHERE id = %s RETURNING *;"
    update_values.append(livro_id)

    cursor.execute(query, tuple(update_values))
    
    # Verifica se algum registro foi atualizado
    if cursor.rowcount == 0:
        conn.rollback() # Reverte a transação se nada foi atualizado
        conn.close()
        return None # Livro não encontrado para atualizar

    conn.commit()
    cursor.close()
    conn.close()
    
    # Após a atualização e commit, busque o livro atualizado para retornar
    return get_livro_by_id_db(livro_id)

def delete_livro_db(livro_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM livros WHERE id = %s RETURNING *;', (livro_id,))
    livro_deletado = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()
    
    return livro_deletado is not None  # Retorna True se o livro foi deletado, False caso contrário