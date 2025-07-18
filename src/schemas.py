from pydantic import BaseModel, Field, ValidationError
from typing import Optional, Literal

class LivroBase(BaseModel):
    titulo: str = Field(..., min_length=1, max_length=255, description="Título do livro")
    autor: str = Field(..., min_length=1, max_length=255, description="Autor do livro")
    ano_publicacao: Optional[int] = Field(None, ge=1, le=2100, description="Ano de publicação do livro (opcional)")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "titulo": "Dom Casmurro",
                "autor": "Machado de Assis",
                "ano_publicacao": 1899
            }
        }

class LivroUpdate(LivroBase):
    titulo: Optional[str] = Field(None, min_length=1, max_length=255, description="Título do livro (opcional para atualização)")
    autor: Optional[str] = Field(None, min_length=1, max_length=255, description="Autor do livro (opcional para atualização)")
    ano_publicacao: Optional[int] = Field(None, ge=1, le=2100, description="Ano de publicação do livro (opcional para atualização)")

    class Config:
        json_schema_extra = {
            "example": {
                "titulo": "Dom Casmurro (Nova Edição)",
                "ano_publicacao": 2023
            }
        }

class MensagemSucesso(BaseModel):
    message: Literal["Livro excluído com sucesso."] = "Livro excluído com sucesso."
