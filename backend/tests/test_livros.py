def test_listar_livros_vazio(client):
    resposta = client.get("/livros/")
    assert resposta.status_code == 200
    assert resposta.json() == []


def test_criar_livro(client, auth_headers):
    client.post("/autores/", json={"nome": "Machado de Assis"}, headers=auth_headers)
    resposta = client.post(
        "/livros/",
        json={"titulo": "Dom Casmurro", "autor_id": 1},
        headers=auth_headers
    )
    assert resposta.status_code == 201
    assert resposta.json()["titulo"] == "Dom Casmurro"
    assert resposta.json()["autor"]["nome"] == "Machado de Assis"


def test_criar_livro_sem_token(client, auth_headers):
    client.post("/autores/", json={"nome": "Machado de Assis"}, headers=auth_headers)
    resposta = client.post(
        "/livros/",
        json={"titulo": "Dom Casmurro", "autor_id": 1}
    )
    assert resposta.status_code == 401


def test_criar_livro_sem_titulo(client, auth_headers):
    client.post("/autores/", json={"nome": "Machado de Assis"}, headers=auth_headers)
    resposta = client.post(
        "/livros/",
        json={"autor_id": 1},
        headers=auth_headers
    )
    assert resposta.status_code == 422


def test_buscar_livro(client, auth_headers):
    client.post("/autores/", json={"nome": "Machado de Assis"}, headers=auth_headers)
    client.post("/livros/", json={"titulo": "Dom Casmurro", "autor_id": 1}, headers=auth_headers)
    resposta = client.get("/livros/1")
    assert resposta.status_code == 200
    assert resposta.json()["titulo"] == "Dom Casmurro"


def test_buscar_livro_inexistente(client):
    resposta = client.get("/livros/999")
    assert resposta.status_code == 404


def test_atualizar_livro(client, auth_headers):
    client.post("/autores/", json={"nome": "Machado de Assis"}, headers=auth_headers)
    client.post("/livros/", json={"titulo": "Dom Casmurro", "autor_id": 1}, headers=auth_headers)
    resposta = client.put(
        "/livros/1",
        json={"ano_publicacao": 1899},
        headers=auth_headers
    )
    assert resposta.status_code == 200
    assert resposta.json()["ano_publicacao"] == 1899


def test_deletar_livro(client, auth_headers):
    client.post("/autores/", json={"nome": "Machado de Assis"}, headers=auth_headers)
    client.post("/livros/", json={"titulo": "Dom Casmurro", "autor_id": 1}, headers=auth_headers)
    resposta = client.delete("/livros/1", headers=auth_headers)
    assert resposta.status_code == 204


def test_deletar_livro_inexistente(client, auth_headers):
    resposta = client.delete("/livros/999", headers=auth_headers)
    assert resposta.status_code == 404