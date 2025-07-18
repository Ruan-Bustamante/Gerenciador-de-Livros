from flask import Blueprint, request, jsonify
from src.models import (
    get_all_livros_orm,
    add_livro_orm,
    get_livro_by_id_orm,
    update_livro_orm,
    delete_livro_orm
)
from src.database import get_db_session
from src.schemas import LivroBase, LivroUpdate, MensagemSucesso
from pydantic import ValidationError

livros_bp = Blueprint('livros', __name__, url_prefix='/livros')

@livros_bp.route('/', methods=['GET'])
def get_livros():
    with get_db_session() as db:
        livros = get_all_livros_orm(db)
        return jsonify([LivroBase.model_validate(l).model_dump() for l in livros])

@livros_bp.route('/', methods=['POST'])
def add_livro():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Nenhum dado fornecido.'}), 400
    
    try:
        novo_livro_data = LivroBase(**data)
    except ValidationError as e:
        return jsonify({"error": "Dados de entrada inválidos", "details": e.errors()}), 400
    
    with get_db_session() as db:
        livro_criado = add_livro_orm(
            db, 
            titulo=novo_livro_data.titulo, 
            autor=novo_livro_data.autor, 
            ano_publicacao=novo_livro_data.ano_publicacao
        )
        return jsonify(LivroBase.model_validate(livro_criado).model_dump()), 201
    
@livros_bp.route('/<int:livro_id>', methods=['GET'])
def get_livro(livro_id):
    with get_db_session() as db:
        livro = get_livro_by_id_orm(db, livro_id)
        if livro is None:
            return jsonify({'error': 'Livro não encontrado'}), 404
        return jsonify(LivroBase.model_validate(livro).model_dump())

@livros_bp.route('/<int:livro_id>', methods=['PUT'])
def update_livro(livro_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Nenhum campo para atualizar fornecido."}), 400
    
    try:
        update_data_pydantic = LivroUpdate(**data)
    except ValidationError as e:
        return jsonify({"error": "Dados de atualização inválidos", "details": e.errors()}), 400

    dados_para_atualizar_db = update_data_pydantic.model_dump(exclude_unset=True)
    
    if not dados_para_atualizar_db:
        return jsonify({"error": "Nenhum campo válido para atualizar fornecido."}), 400

    with get_db_session() as db:
        livro_atualizado = update_livro_orm(db, livro_id, dados_para_atualizar_db)
        if livro_atualizado is None:
            return jsonify({"error": "Livro não encontrado"}), 404
        return jsonify(LivroBase.model_validate(livro_atualizado).model_dump())

    
@livros_bp.route('/<int:livro_id>', methods=['DELETE'])
def delete_livro(livro_id):
    with get_db_session() as db:
        deleted = delete_livro_orm(db, livro_id)
        if not deleted:
            return jsonify({'error': 'Livro não encontrado'}), 404
        return jsonify(MensagemSucesso(message="Livro excluído com sucesso.").model_dump()), 204