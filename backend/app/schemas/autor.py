from pydantic import BaseModel
from datetime import date
from typing import Optional


class AutorBase(BaseModel):
    nome: str
    biografia: Optional[str] = None
    foto_url: Optional[str] = None
    nacionalidade: Optional[str] = None
    data_nascimento: Optional[date] = None
    data_morte: Optional[date] = None


class AutorCreate(AutorBase):
    pass


class AutorUpdate(AutorBase):
    nome: Optional[str] = None


class AutorResponse(AutorBase):
    id: int

    class Config:
        from_attributes = True