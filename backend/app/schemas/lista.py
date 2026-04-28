from pydantic import BaseModel
from typing import Optional


class ListaBase(BaseModel):
    titulo: str
    fonte: Optional[str] = None
    ano: Optional[int] = None
    descricao: Optional[str] = None


class ListaCreate(ListaBase):
    pass


class ListaUpdate(ListaBase):
    titulo: Optional[str] = None


class ListaResponse(ListaBase):
    id: int

    class Config:
        from_attributes = True


class LivroListaBase(BaseModel):
    livro_id: int
    lista_id: int
    posicao: Optional[int] = None
    redator: Optional[str] = None


class LivroListaCreate(LivroListaBase):
    pass


class LivroListaUpdate(BaseModel):
    posicao: Optional[int] = None
    redator: Optional[str] = None


class LivroListaResponse(LivroListaBase):
    class Config:
        from_attributes = True