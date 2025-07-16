from flask import Flask
from src.database import create_tables
from src.routes import livros_bp

app = Flask(__name__)

# Registra o Blueprint para as rotas de livros
app.register_blueprint(livros_bp)

# Garante que o banco de dados esteja inicializado

with app.app_context():
    create_tables()

# Executa a aplicação

if __name__ == '__main__':
    app.run(debug=True) # debug=True para desenvolvimento, desative em produção