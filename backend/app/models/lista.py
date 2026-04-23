from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Lista(Base):
    __tablename__ = "listas"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(255), nullable=False)
    fonte = Column(String(255), nullable=True)
    ano = Column(Integer, nullable=True)
    descricao = Column(Text, nullable=True)

    livros = relationship("LivroLista", back_populates="lista")


class LivroLista(Base):
    __tablename__ = "livros_lista"

    livro_id = Column(Integer, ForeignKey("livros.id"), primary_key=True)
    lista_id = Column(Integer, ForeignKey("listas.id"), primary_key=True)
    redator = Column(String(255), primary_key=True, default="")
    posicao = Column(Integer, nullable=True)

    livro = relationship("Livro", back_populates="listas")
    lista = relationship("Lista", back_populates="livros")