from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.lista import Lista, LivroLista
from app.schemas.lista import (
    ListaCreate, ListaUpdate, ListaResponse,
    LivroListaCreate, LivroListaUpdate, LivroListaResponse
)
from typing import List
from app.auth import verificar_token

router = APIRouter()


# --- Lista ---

@router.get("/", response_model=List[ListaResponse])
def listar_listas(db: Session = Depends(get_db)):
    return db.query(Lista).all()


@router.get("/{id}", response_model=ListaResponse)
def buscar_lista(id: int, db: Session = Depends(get_db)):
    lista = db.query(Lista).filter(Lista.id == id).first()
    if not lista:
        raise HTTPException(status_code=404, detail="Lista não encontrada")
    return lista


@router.post("/", response_model=ListaResponse, status_code=201)
def criar_lista(lista: ListaCreate, db: Session = Depends(get_db), usuario: str = Depends(verificar_token)):
    nova = Lista(**lista.model_dump())
    db.add(nova)
    db.commit()
    db.refresh(nova)
    return nova


@router.put("/{id}", response_model=ListaResponse)
def atualizar_lista(id: int, dados: ListaUpdate, db: Session = Depends(get_db), usuario: str = Depends(verificar_token)):
    lista = db.query(Lista).filter(Lista.id == id).first()
    if not lista:
        raise HTTPException(status_code=404, detail="Lista não encontrada")
    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(lista, campo, valor)
    db.commit()
    db.refresh(lista)
    return lista


@router.delete("/{id}", status_code=204)
def deletar_lista(id: int, db: Session = Depends(get_db), usuario: str = Depends(verificar_token)):
    lista = db.query(Lista).filter(Lista.id == id).first()
    if not lista:
        raise HTTPException(status_code=404, detail="Lista não encontrada")
    db.delete(lista)
    db.commit()


# --- LivroLista ---

@router.get("/{lista_id}/livros", response_model=List[LivroListaResponse])
def listar_livros_da_lista(lista_id: int, db: Session = Depends(get_db)):
    return db.query(LivroLista).filter(LivroLista.lista_id == lista_id).all()


@router.post("/{lista_id}/livros", response_model=LivroListaResponse, status_code=201)
def adicionar_livro_lista(lista_id: int, dados: LivroListaCreate, db: Session = Depends(get_db), usuario: str = Depends(verificar_token)):
    novo = LivroLista(**dados.model_dump())
    db.add(novo)
    db.commit()
    return novo


@router.put("/{lista_id}/livros/{livro_id}", response_model=LivroListaResponse)
def atualizar_livro_lista(lista_id: int, livro_id: int, dados: LivroListaUpdate, db: Session = Depends(get_db), usuario: str = Depends(verificar_token)):
    livro_lista = db.query(LivroLista).filter(
        LivroLista.lista_id == lista_id,
        LivroLista.livro_id == livro_id
    ).first()
    if not livro_lista:
        raise HTTPException(status_code=404, detail="Relação não encontrada")
    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(livro_lista, campo, valor)
    db.commit()
    return livro_lista


@router.delete("/{lista_id}/livros/{livro_id}", status_code=204)
def remover_livro_lista(lista_id: int, livro_id: int, db: Session = Depends(get_db), usuario: str = Depends(verificar_token)):
    livro_lista = db.query(LivroLista).filter(
        LivroLista.lista_id == lista_id,
        LivroLista.livro_id == livro_id
    ).first()
    if not livro_lista:
        raise HTTPException(status_code=404, detail="Relação não encontrada")
    db.delete(livro_lista)
    db.commit()