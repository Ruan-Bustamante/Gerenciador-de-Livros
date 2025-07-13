from flask import Blueprint, request, jsonify
from src.models import (
    get_all_livros_db,
    add_livro_db,
    get_livro_by_id_db,
    update_livro_db,
    delete_livro_db
)

# Define o Blueprint para as rotas de livros
livros_bp = Blueprint('livros', __name__, url_prefix='/livros')

@livros_bp.route('/', methods=['GET'])
def get_livros():
    livros = get_all_livros_db()
    return jsonify(livros)

@livros_bp.route('/', methods=['POST'])
def add_livro():
    novo_livro = request.get_json()
    if not novo_livro or 'titulo' not in novo_livro or 'autor' not in novo_livro:
        return jsonify({"error": "Dados inválidos. 'titulo', 'autor' e 'ano_publicacao' são obrigatórios."}), 400
    
    titulo = novo_livro['titulo']
    autor = novo_livro['autor']
    ano_publicacao = novo_livro['ano_publicacao']

    try:
        ano_publicacao = int(ano_publicacao)
    except ValueError:
        return jsonify({"error": "Ano de publicação deve ser um número inteiro."}), 400
    
    livro = add_livro_db(titulo, autor, ano_publicacao)
    return jsonify(livro), 201

@livros_bp.route('/<int:livro_id>', methods=['GET'])
def get_livro(livro_id):
    livro = get_livro_by_id_db(livro_id)
    if livro is None:
        return jsonify({"error": "Livro não encontrado"}), 404
    return jsonify(livro)

@livros_bp.route('/<int:livro_id>', methods=['PUT'])
def update_livro(livro_id):
    dados_atualizados = request.get_json()
    if not dados_atualizados:
        return jsonify({"error": "Nenhum campo para atualizar fornecido."}), 400

    # Validação básica para ano_publicacao se estiver presente
    if 'ano_publicacao' in dados_atualizados:
        try:
            dados_atualizados['ano_publicacao'] = int(dados_atualizados['ano_publicacao'])
        except ValueError:
            return jsonify({"error": "Ano de publicação deve ser um número inteiro."}), 400

    livro = update_livro_db(livro_id, dados_atualizados)
    if livro is None:
        return jsonify({"error": "Livro não encontrado ou nenhum campo válido para atualizar."}), 404
    return jsonify(livro)

@livros_bp.route('/<int:livro_id>', methods=['DELETE'])
def delete_livro(livro_id):
    livro_deletado = delete_livro_db(livro_id)
    if livro_deletado is None:
        return jsonify({"error": "Livro não encontrado"}), 404
    return jsonify({"message": "Livro deletado com sucesso", "livro": livro_deletado}), 200