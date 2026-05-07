def test_listar_listas_vazio(client):
    resposta = client.get("/listas/")
    assert resposta.status_code == 200
    assert resposta.json() == []


def test_criar_lista(client, auth_headers):
    resposta = client.post(
        "/listas/",
        json={"titulo": "10 melhores de 2023", "fonte": "Revista Quatro Cinco Um"},
        headers=auth_headers
    )
    assert resposta.status_code == 201
    assert resposta.json()["titulo"] == "10 melhores de 2023"


def test_criar_lista_sem_token(client):
    resposta = client.post(
        "/listas/",
        json={"titulo": "10 melhores de 2023"}
    )
    assert resposta.status_code == 401


def test_criar_lista_sem_titulo(client, auth_headers):
    resposta = client.post(
        "/listas/",
        json={"fonte": "Revista Quatro Cinco Um"},
        headers=auth_headers
    )
    assert resposta.status_code == 422


def test_buscar_lista(client, auth_headers):
    client.post("/listas/", json={"titulo": "10 melhores de 2023"}, headers=auth_headers)
    resposta = client.get("/listas/1")
    assert resposta.status_code == 200
    assert resposta.json()["titulo"] == "10 melhores de 2023"


def test_buscar_lista_inexistente(client):
    resposta = client.get("/listas/999")
    assert resposta.status_code == 404


def test_adicionar_livro_lista(client, auth_headers):
    client.post("/autores/", json={"nome": "Machado de Assis"}, headers=auth_headers)
    client.post("/livros/", json={"titulo": "Dom Casmurro", "autor_id": 1}, headers=auth_headers)
    client.post("/listas/", json={"titulo": "10 melhores de 2023"}, headers=auth_headers)
    resposta = client.post(
        "/listas/1/livros",
        json={"livro_id": 1, "lista_id": 1, "posicao": 1},
        headers=auth_headers
    )
    assert resposta.status_code == 201


def test_atualizar_lista(client, auth_headers):
    client.post("/listas/", json={"titulo": "10 melhores de 2023"}, headers=auth_headers)
    resposta = client.put(
        "/listas/1",
        json={"descricao": "Seleção anual da crítica literária."},
        headers=auth_headers
    )
    assert resposta.status_code == 200
    assert resposta.json()["descricao"] == "Seleção anual da crítica literária."


def test_deletar_lista(client, auth_headers):
    client.post("/listas/", json={"titulo": "10 melhores de 2023"}, headers=auth_headers)
    resposta = client.delete("/listas/1", headers=auth_headers)
    assert resposta.status_code == 204


def test_deletar_lista_inexistente(client, auth_headers):
    resposta = client.delete("/listas/999", headers=auth_headers)
    assert resposta.status_code == 404