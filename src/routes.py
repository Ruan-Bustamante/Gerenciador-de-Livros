from flask import Blueprint, request, jsonify
from src.models import (
    Livro,
    get_all_livros_orm,
    add_livro_orm,
    get_livro_by_id_orm,
    update_livro_orm,
    delete_livro_orm
)
from src.database import get_db_session

livros_bp = Blueprint('livros', __name__, url_prefix='/livros')

@livros_bp.route('/', methods=['GET'])
def get_livros():
    with get_db_session() as db:
        livros = get_all_livros_orm(db)
        return jsonify([{'id': l.id, 'titulo': l.titulo, 'autor': l.autor, 'ano_publicacao': l.ano_publicacao} for l in livros])
    
@livros_bp.route('/', methods=['POST'])
def add_livro():
    novo_livro_data = request.get_json()
    if not novo_livro_data or 'titulo' not in novo_livro_data or 'autor' not in novo_livro_data:
        return jsonify({'error': 'Dados inválidos. Titulo e autor são obrigatórios'}), 400
    
    titulo = novo_livro_data['titulo']
    autor = novo_livro_data['autor']
    ano_publicacao = novo_livro_data.get('ano_publicacao')

    if ano_publicacao is not None:
        try:
            ano_publicacao = int(ano_publicacao)
        except ValueError:
            return jsonify({'error': 'Ano de publicação deve ser um número inteiro'}), 400
    
    with get_db_session() as db:
        livro_criado = add_livro_orm(db, titulo, autor, ano_publicacao)
        return jsonify({
            "id": livro_criado.id,
            "titulo": livro_criado.titulo,
            "autor": livro_criado.autor,
            "ano_publicacao": livro_criado.ano_publicacao
        }), 201
    
@livros_bp.route('/<int:livro_id>', methods=['GET'])
def get_livro(livro_id):
    with get_db_session() as db:
        livro = get_livro_by_id_orm(db, livro_id)
        if livro is None:
            return jsonify({'error': 'Livro não encontrado'}), 404
        return jsonify({
            "id": livro.id,
            "titulo": livro.titulo,
            "autor": livro.autor,
            "ano_publicacao": livro.ano_publicacao
        })

@livros_bp.route('/<int:livro_id>', methods=['PUT'])
def update_livro(livro_id):
    update_data = request.get_json()
    if not update_data:
        return jsonify({'error': 'Nenhum campo para atualizar fornecido'}), 400
    
    if 'ano_publicacao' in update_data and update_data['ano_publicacao'] is not None:
        try:
            update_data['ano_publicacao'] = int(update_data['ano_publicacao'])
        except ValueError:
            return jsonify({'error': 'Ano de publicação deve ser um número inteiro'}), 400
    
    with get_db_session() as db:
        livro_atualizado = update_livro_orm(db, livro_id, update_data)
        if livro_atualizado is None:
            return jsonify({'error': 'Livro não encontrado'}), 404
        return jsonify({
            "id": livro_atualizado.id,
            "titulo": livro_atualizado.titulo,
            "autor": livro_atualizado.autor,
            "ano_publicacao": livro_atualizado.ano_publicacao
        })

@livros_bp.route('/<int:livro_id>', methods=['DELETE'])
def delete_livro(livro_id):
    with get_db_session() as db:
        deleted = delete_livro_orm(db, livro_id)
        if not deleted:
            return jsonify({'error': 'Livro não encontrado'}), 404
        return jsonify({'message':  f'Livro com ID {livro_id} excluído com sucesso.'}), 204