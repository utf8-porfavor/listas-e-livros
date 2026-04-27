from pydantic import BaseModel
from datetime import date
from typing import Optional


class LivroBase(BaseModel):
    titulo: str
    subtitulo: Optional[str] = None
    autor_id: int
    isbn: Optional[str] = None
    ano_publicacao: Optional[int] = None
    editora: Optional[str] = None
    idioma_original: Optional[str] = None
    descricao: Optional[str] = None
    capa_url: Optional[str] = None
    link_afiliado: Optional[str] = None
    short_url: Optional[str] = None
    tradutor: Optional[str] = None
    ativo: Optional[int] = 1


class LivroCreate(LivroBase):
    pass


class LivroUpdate(LivroBase):
    titulo: Optional[str] = None
    autor_id: Optional[int] = None


class LivroResponse(LivroBase):
    id: int
    autor: Optional[str] = None

    class Config:
        from_attributes = True