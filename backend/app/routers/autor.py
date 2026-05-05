from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.autor import Autor
from app.schemas.autor import AutorCreate, AutorUpdate, AutorResponse
from typing import List
from app.auth import verificar_token

router = APIRouter()


@router.get("/", response_model=List[AutorResponse])
def listar_autores(db: Session = Depends(get_db)):
    return db.query(Autor).all()


@router.get("/{id}", response_model=AutorResponse)
def buscar_autor(id: int, db: Session = Depends(get_db)):
    autor = db.query(Autor).filter(Autor.id == id).first()
    if not autor:
        raise HTTPException(status_code=404, detail="Autor não encontrado")
    return autor


@router.post("/", response_model=AutorResponse, status_code=201)
def criar_autor(autor: AutorCreate, db: Session = Depends(get_db), usuario: str = Depends(verificar_token)):
    novo_autor = Autor(**autor.model_dump())
    db.add(novo_autor)
    db.commit()
    db.refresh(novo_autor)
    return novo_autor


@router.put("/{id}", response_model=AutorResponse)
def atualizar_autor(id: int, dados: AutorUpdate, db: Session = Depends(get_db), usuario: str = Depends(verificar_token)):
    autor = db.query(Autor).filter(Autor.id == id).first()
    if not autor:
        raise HTTPException(status_code=404, detail="Autor não encontrado")
    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(autor, campo, valor)
    db.commit()
    db.refresh(autor)
    return autor


@router.delete("/{id}", status_code=204)
def deletar_autor(id: int, db: Session = Depends(get_db), usuario: str = Depends(verificar_token)):
    autor = db.query(Autor).filter(Autor.id == id).first()
    if not autor:
        raise HTTPException(status_code=404, detail="Autor não encontrado")
    db.delete(autor)
    db.commit()