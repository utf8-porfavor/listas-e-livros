from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Premio(Base):
    __tablename__ = "premios"

    id = Column(Integer, primary_key=True)
    nome = Column(String(255), nullable=False)
    descricao = Column(Text, nullable=True)
    tipo = Column(String(50), nullable=False)  # "livro" ou "autor"

    edicoes = relationship("EdicaoPremio", back_populates="premio")


class EdicaoPremio(Base):
    __tablename__ = "edicoes_premio"

    id = Column(Integer, primary_key=True)
    premio_id = Column(Integer, ForeignKey("premios.id"), nullable=False)
    ano = Column(Integer, nullable=False)
    descricao = Column(Text, nullable=True)

    premio = relationship("Premio", back_populates="edicoes")
    categorias = relationship("CategoriaPremio", back_populates="edicao")
    autores_premiados = relationship("AutorPremio", back_populates="edicao")


class CategoriaPremio(Base):
    __tablename__ = "categorias_premio"

    id = Column(Integer, primary_key=True)
    edicao_id = Column(Integer, ForeignKey("edicoes_premio.id"), nullable=False)
    nome = Column(String(255), nullable=False)

    edicao = relationship("EdicaoPremio", back_populates="categorias")
    livros = relationship("LivroCategoria", back_populates="categoria")


class LivroCategoria(Base):
    __tablename__ = "livros_categoria"

    livro_id = Column(Integer, ForeignKey("livros.id"), primary_key=True)
    categoria_id = Column(Integer, ForeignKey("categorias_premio.id"), primary_key=True)
    colocacao = Column(String(50), nullable=True)  # "Vencedor", "Finalista"

    livro = relationship("Livro", back_populates="categorias_premio")
    categoria = relationship("CategoriaPremio", back_populates="livros")


class AutorPremio(Base):
    __tablename__ = "autores_premio"

    autor_id = Column(Integer, ForeignKey("autores.id"), primary_key=True)
    edicao_id = Column(Integer, ForeignKey("edicoes_premio.id"), primary_key=True)
    colocacao = Column(String(50), nullable=True)  # "Vencedor", "Finalista"

    autor = relationship("Autor", back_populates="premios")
    edicao = relationship("EdicaoPremio", back_populates="autores_premiados")