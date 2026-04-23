from sqlalchemy import Column, Integer, String, Date, Text
from sqlalchemy.orm import relationship
from app.database import Base


class Autor(Base):
    __tablename__ = "autores"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    biografia = Column(Text, nullable=True)
    foto_url = Column(String(500), nullable=True)
    nacionalidade = Column(String(100), nullable=True)
    data_nascimento = Column(Date, nullable=True)
    data_morte = Column(Date, nullable=True)

    livros = relationship("Livro", back_populates="autor")
    premios = relationship("AutorPremio", back_populates="autor")