from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import autor
from app.routers import livro

app = FastAPI(title="Listas e Livros")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(autor.router, prefix="/autores", tags=["Autores"])
app.include_router(livro.router, prefix="/livros", tags=["Livros"])


@app.get("/")
def root():
    return {"status": "ok"}