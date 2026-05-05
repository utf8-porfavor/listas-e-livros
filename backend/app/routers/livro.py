from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.livro import Livro
from app.schemas.livro import LivroCreate, LivroUpdate, LivroResponse
from typing import List
from app.auth import verificar_token

router = APIRouter()


@router.get("/", response_model=List[LivroResponse])
def listar_livros(db: Session = Depends(get_db)):
    return db.query(Livro).all()


@router.get("/{id}", response_model=LivroResponse)
def buscar_livro(id: int, db: Session = Depends(get_db)):
    livro = db.query(Livro).filter(Livro.id == id).first()
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return livro


@router.post("/", response_model=LivroResponse, status_code=201)
def criar_livro(livro: LivroCreate, db: Session = Depends(get_db), usuario: str = Depends(verificar_token)):
    novo_livro = Livro(**livro.model_dump())
    db.add(novo_livro)
    db.commit()
    db.refresh(novo_livro)
    return novo_livro


@router.put("/{id}", response_model=LivroResponse)
def atualizar_livro(id: int, dados: LivroUpdate, db: Session = Depends(get_db), usuario: str = Depends(verificar_token)):
    livro = db.query(Livro).filter(Livro.id == id).first()
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(livro, campo, valor)
    db.commit()
    db.refresh(livro)
    return livro


@router.delete("/{id}", status_code=204)
def deletar_livro(id: int, db: Session = Depends(get_db), usuario: str = Depends(verificar_token)):
    livro = db.query(Livro).filter(Livro.id == id).first()
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    db.delete(livro)
    db.commit()