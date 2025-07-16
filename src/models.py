from sqlalchemy import Column, Integer, String
from src.database import Base
from sqlalchemy.orm import Session
from typing import List, Optional

class Livro(Base):
    __tablename__ = 'livros'
    
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    autor = Column(String, nullable=False)
    ano_publicacao = Column(Integer, nullable=True)

    def __repr__(self):
        return f"<Livro(id={self.id}, titulo='{self.titulo}', autor='{self.autor}', ano_publicacao={self.ano_publicacao})>"

# Funções CRUD usando SQLAlchemy ORM

def get_all_livros_orm(db: Session) -> List[Livro]:
    return db.query(Livro).all()

def add_livro_orm(db: Session, titulo: str, autor: str, ano_publicacao: Optional[int] = None) -> Livro:
    novo_livro = Livro(titulo=titulo, autor=autor, ano_publicacao=ano_publicacao)
    db.add(novo_livro)
    db.commit()
    db.refresh(novo_livro)
    return novo_livro

def get_livro_by_id_orm(db: Session, livro_id: int) -> Optional[Livro]:
    return db.query(Livro).filter(Livro.id == livro_id).first()

def update_livro_orm(db: Session, livro_id: int,  dados_atualizados: dict) -> Optional[Livro]:
    livro = db.query(Livro).filter(Livro.id == livro_id).first()
    if livro:
        for key, value in dados_atualizados.items():
            if hasattr(livro, key):
                setattr(livro, key, value)
        
        db.commit()
        db.refresh(livro)
        return livro
    return None

def delete_livro_orm(db: Session, livro_id: int) -> bool:
    livro = db.query(Livro).filter(Livro.id == livro_id).first()
    if livro:
        db.delete(livro)
        db.commit()
        return True
    return False
