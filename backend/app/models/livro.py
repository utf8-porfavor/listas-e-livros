from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Livro(Base):
    __tablename__ = "livros"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(255), nullable=False)
    subtitulo = Column(String(255), nullable=True)
    autor_id = Column(Integer, ForeignKey("autores.id"), nullable=False)
    isbn = Column(String(20), nullable=True)
    ano_publicacao = Column(Integer, nullable=True)
    editora = Column(String(255), nullable=True)
    idioma_original = Column(String(100), nullable=True)
    descricao = Column(Text, nullable=True)
    capa_url = Column(String(500), nullable=True)
    link_afiliado = Column(String(500), nullable=True)
    short_url = Column(String(100), nullable=True)
    ativo = Column(Integer, default=1)

    autor = relationship("Autor", back_populates="livros")
    categorias_premio = relationship("LivroCategoria", back_populates="livro")
    listas = relationship("LivroLista", back_populates="livro")