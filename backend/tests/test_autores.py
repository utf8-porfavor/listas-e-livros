def test_listar_autores_vazio(client):
    resposta = client.get("/autores/")
    assert resposta.status_code == 200
    assert resposta.json() == []


def test_criar_autor(client, auth_headers):
    resposta = client.post(
        "/autores/",
        json={"nome": "Machado de Assis"},
        headers=auth_headers
    )
    assert resposta.status_code == 201
    assert resposta.json()["nome"] == "Machado de Assis"
    assert resposta.json()["id"] == 1


def test_criar_autor_sem_token(client):
    resposta = client.post(
        "/autores/",
        json={"nome": "Machado de Assis"}
    )
    assert resposta.status_code == 401


def test_criar_autor_sem_nome(client, auth_headers):
    resposta = client.post(
        "/autores/",
        json={"nacionalidade": "Brasileira"},
        headers=auth_headers
    )
    assert resposta.status_code == 422


def test_buscar_autor(client, auth_headers):
    client.post(
        "/autores/",
        json={"nome": "Machado de Assis"},
        headers=auth_headers
    )
    resposta = client.get("/autores/1")
    assert resposta.status_code == 200
    assert resposta.json()["nome"] == "Machado de Assis"


def test_buscar_autor_inexistente(client):
    resposta = client.get("/autores/999")
    assert resposta.status_code == 404


def test_atualizar_autor(client, auth_headers):
    client.post(
        "/autores/",
        json={"nome": "Machado de Assis"},
        headers=auth_headers
    )
    resposta = client.put(
        "/autores/1",
        json={"biografia": "Um dos maiores escritores brasileiros."},
        headers=auth_headers
    )
    assert resposta.status_code == 200
    assert resposta.json()["biografia"] == "Um dos maiores escritores brasileiros."


def test_deletar_autor(client, auth_headers):
    client.post(
        "/autores/",
        json={"nome": "Machado de Assis"},
        headers=auth_headers
    )
    resposta = client.delete("/autores/1", headers=auth_headers)
    assert resposta.status_code == 204


def test_deletar_autor_inexistente(client, auth_headers):
    resposta = client.delete("/autores/999", headers=auth_headers)
    assert resposta.status_code == 404