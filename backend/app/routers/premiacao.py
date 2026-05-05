from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.premiacao import Premio, EdicaoPremio, CategoriaPremio, LivroCategoria, AutorPremio
from app.schemas.premiacao import (
    PremioCreate, PremioUpdate, PremioResponse,
    EdicaoPremioCreate, EdicaoPremioUpdate, EdicaoPremioResponse,
    CategoriaPremioCreate, CategoriaPremioUpdate, CategoriaPremioResponse,
    LivroCategoriaCreate, LivroCategoriaUpdate, LivroCategoriaResponse,
    AutorPremioCreate, AutorPremioUpdate, AutorPremioResponse
)
from typing import List
from app.auth import verificar_token
router = APIRouter()


# --- Premio ---

@router.get("/", response_model=List[PremioResponse])
def listar_premios(db: Session = Depends(get_db)):
    return db.query(Premio).all()


@router.get("/{id}", response_model=PremioResponse)
def buscar_premio(id: int, db: Session = Depends(get_db)):
    premio = db.query(Premio).filter(Premio.id == id).first()
    if not premio:
        raise HTTPException(status_code=404, detail="Prêmio não encontrado")
    return premio


@router.post("/", response_model=PremioResponse, status_code=201)
def criar_premio(premio: PremioCreate, db: Session = Depends(get_db), usuario: str = Depends(verificar_token)):
    novo = Premio(**premio.model_dump())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo


@router.put("/{id}", response_model=PremioResponse)
def atualizar_premio(id: int, dados: PremioUpdate, db: Session = Depends(get_db), usuario: str = Depends(verificar_token)):
    premio = db.query(Premio).filter(Premio.id == id).first()
    if not premio:
        raise HTTPException(status_code=404, detail="Prêmio não encontrado")
    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(premio, campo, valor)
    db.commit()
    db.refresh(premio)
    return premio


@router.delete("/{id}", status_code=204)
def deletar_premio(id: int, db: Session = Depends(get_db), usuario: str = Depends(verificar_token)):
    premio = db.query(Premio).filter(Premio.id == id).first()
    if not premio:
        raise HTTPException(status_code=404, detail="Prêmio não encontrado")
    db.delete(premio)
    db.commit()


# --- EdicaoPremio ---

@router.get("/{premio_id}/edicoes", response_model=List[EdicaoPremioResponse])
def listar_edicoes(premio_id: int, db: Session = Depends(get_db)):
    return db.query(EdicaoPremio).filter(EdicaoPremio.premio_id == premio_id).all()


@router.post("/{premio_id}/edicoes", response_model=EdicaoPremioResponse, status_code=201)
def criar_edicao(premio_id: int, edicao: EdicaoPremioCreate, db: Session = Depends(get_db), usuario: str = Depends(verificar_token)):
    nova = EdicaoPremio(**edicao.model_dump())
    db.add(nova)
    db.commit()
    db.refresh(nova)
    return nova


@router.put("/edicoes/{id}", response_model=EdicaoPremioResponse)
def atualizar_edicao(id: int, dados: EdicaoPremioUpdate, db: Session = Depends(get_db), usuario: str = Depends(verificar_token)):
    edicao = db.query(EdicaoPremio).filter(EdicaoPremio.id == id).first()
    if not edicao:
        raise HTTPException(status_code=404, detail="Edição não encontrada")
    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(edicao, campo, valor)
    db.commit()
    db.refresh(edicao)
    return edicao


@router.delete("/edicoes/{id}", status_code=204)
def deletar_edicao(id: int, db: Session = Depends(get_db), usuario: str = Depends(verificar_token)):
    edicao = db.query(EdicaoPremio).filter(EdicaoPremio.id == id).first()
    if not edicao:
        raise HTTPException(status_code=404, detail="Edição não encontrada")
    db.delete(edicao)
    db.commit()


# --- CategoriaPremio ---

@router.get("/edicoes/{edicao_id}/categorias", response_model=List[CategoriaPremioResponse])
def listar_categorias(edicao_id: int, db: Session = Depends(get_db)):
    return db.query(CategoriaPremio).filter(CategoriaPremio.edicao_id == edicao_id).all()


@router.post("/edicoes/{edicao_id}/categorias", response_model=CategoriaPremioResponse, status_code=201)
def criar_categoria(edicao_id: int, categoria: CategoriaPremioCreate, db: Session = Depends(get_db), usuario: str = Depends(verificar_token)):
    nova = CategoriaPremio(**categoria.model_dump())
    db.add(nova)
    db.commit()
    db.refresh(nova)
    return nova


@router.put("/edicoes/{edicao_id}/categorias/{id}", response_model=CategoriaPremioResponse)
def atualizar_categoria(edicao_id: int, id: int, dados: CategoriaPremioUpdate, db: Session = Depends(get_db), usuario: str = Depends(verificar_token)):
    categoria = db.query(CategoriaPremio).filter(
        CategoriaPremio.id == id,
        CategoriaPremio.edicao_id == edicao_id
    ).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(categoria, campo, valor)
    db.commit()
    db.refresh(categoria)
    return categoria


@router.delete("/edicoes/{edicao_id}/categorias/{id}", status_code=204)
def deletar_categoria(edicao_id: int, id: int, db: Session = Depends(get_db), usuario: str = Depends(verificar_token)):
    categoria = db.query(CategoriaPremio).filter(
        CategoriaPremio.id == id,
        CategoriaPremio.edicao_id == edicao_id
    ).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    db.delete(categoria)
    db.commit()

# --- LivroCategoria ---

@router.post("/categorias/{categoria_id}/livros", response_model=LivroCategoriaResponse, status_code=201)
def adicionar_livro_categoria(categoria_id: int, dados: LivroCategoriaCreate, db: Session = Depends(get_db), usuario: str = Depends(verificar_token)):
    novo = LivroCategoria(**dados.model_dump())
    db.add(novo)
    db.commit()
    return novo


@router.delete("/categorias/{categoria_id}/livros/{livro_id}", status_code=204)
def remover_livro_categoria(categoria_id: int, livro_id: int, db: Session = Depends(get_db), usuario: str = Depends(verificar_token)):
    livro_cat = db.query(LivroCategoria).filter(
        LivroCategoria.categoria_id == categoria_id,
        LivroCategoria.livro_id == livro_id
    ).first()
    if not livro_cat:
        raise HTTPException(status_code=404, detail="Relação não encontrada")
    db.delete(livro_cat)
    db.commit()


# --- AutorPremio ---

@router.post("/edicoes/{edicao_id}/autores", response_model=AutorPremioResponse, status_code=201)
def adicionar_autor_premio(edicao_id: int, dados: AutorPremioCreate, db: Session = Depends(get_db), usuario: str = Depends(verificar_token)):
    novo = AutorPremio(**dados.model_dump())
    db.add(novo)
    db.commit()
    return novo


@router.delete("/edicoes/{edicao_id}/autores/{autor_id}", status_code=204)
def remover_autor_premio(edicao_id: int, autor_id: int, db: Session = Depends(get_db), usuario: str = Depends(verificar_token)):
    autor_premio = db.query(AutorPremio).filter(
        AutorPremio.edicao_id == edicao_id,
        AutorPremio.autor_id == autor_id
    ).first()
    if not autor_premio:
        raise HTTPException(status_code=404, detail="Relação não encontrada")
    db.delete(autor_premio)
    db.commit()