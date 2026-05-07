from pydantic import BaseModel, ConfigDict
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

    model_config = ConfigDict(from_attributes=True)