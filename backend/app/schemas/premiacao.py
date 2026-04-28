from pydantic import BaseModel
from typing import Optional


class PremioBase(BaseModel):
    nome: str
    descricao: Optional[str] = None
    tipo: str  # "livro" ou "autor"


class PremioCreate(PremioBase):
    pass


class PremioUpdate(PremioBase):
    nome: Optional[str] = None
    tipo: Optional[str] = None


class PremioResponse(PremioBase):
    id: int

    class Config:
        from_attributes = True


class EdicaoPremioBase(BaseModel):
    premio_id: int
    ano: int
    descricao: Optional[str] = None


class EdicaoPremioCreate(EdicaoPremioBase):
    pass


class EdicaoPremioUpdate(EdicaoPremioBase):
    premio_id: Optional[int] = None
    ano: Optional[int] = None


class EdicaoPremioResponse(EdicaoPremioBase):
    id: int

    class Config:
        from_attributes = True


class CategoriaPremioBase(BaseModel):
    edicao_id: int
    nome: str


class CategoriaPremioCreate(CategoriaPremioBase):
    pass


class CategoriaPremioUpdate(CategoriaPremioBase):
    edicao_id: Optional[int] = None
    nome: Optional[str] = None


class CategoriaPremioResponse(CategoriaPremioBase):
    id: int

    class Config:
        from_attributes = True


class LivroCategoriaBase(BaseModel):
    livro_id: int
    categoria_id: int
    colocacao: Optional[str] = None  # "winner", "shortlist", "longlist"


class LivroCategoriaCreate(LivroCategoriaBase):
    pass


class LivroCategoriaUpdate(BaseModel):
    colocacao: Optional[str] = None


class LivroCategoriaResponse(LivroCategoriaBase):
    class Config:
        from_attributes = True


class AutorPremioBase(BaseModel):
    autor_id: int
    edicao_id: int
    colocacao: Optional[str] = None


class AutorPremioCreate(AutorPremioBase):
    pass


class AutorPremioUpdate(BaseModel):
    colocacao: Optional[str] = None


class AutorPremioResponse(AutorPremioBase):
    class Config:
        from_attributes = True