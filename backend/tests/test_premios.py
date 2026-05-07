def test_listar_premios_vazio(client):
    resposta = client.get("/premios/")
    assert resposta.status_code == 200
    assert resposta.json() == []


def test_criar_premio(client, auth_headers):
    resposta = client.post(
        "/premios/",
        json={"nome": "Prêmio Jabuti", "tipo": "livro"},
        headers=auth_headers
    )
    assert resposta.status_code == 201
    assert resposta.json()["nome"] == "Prêmio Jabuti"


def test_criar_premio_sem_token(client):
    resposta = client.post(
        "/premios/",
        json={"nome": "Prêmio Jabuti", "tipo": "livro"}
    )
    assert resposta.status_code == 401


def test_buscar_premio(client, auth_headers):
    client.post("/premios/", json={"nome": "Prêmio Jabuti", "tipo": "livro"}, headers=auth_headers)
    resposta = client.get("/premios/1")
    assert resposta.status_code == 200
    assert resposta.json()["nome"] == "Prêmio Jabuti"


def test_buscar_premio_inexistente(client):
    resposta = client.get("/premios/999")
    assert resposta.status_code == 404


def test_criar_edicao(client, auth_headers):
    client.post("/premios/", json={"nome": "Prêmio Jabuti", "tipo": "livro"}, headers=auth_headers)
    resposta = client.post(
        "/premios/1/edicoes",
        json={"premio_id": 1, "ano": 2024},
        headers=auth_headers
    )
    assert resposta.status_code == 201
    assert resposta.json()["ano"] == 2024


def test_criar_categoria(client, auth_headers):
    client.post("/premios/", json={"nome": "Prêmio Jabuti", "tipo": "livro"}, headers=auth_headers)
    client.post("/premios/1/edicoes", json={"premio_id": 1, "ano": 2024}, headers=auth_headers)
    resposta = client.post(
        "/premios/edicoes/1/categorias",
        json={"edicao_id": 1, "nome": "Ficção"},
        headers=auth_headers
    )
    assert resposta.status_code == 201
    assert resposta.json()["nome"] == "Ficção"


def test_atualizar_premio(client, auth_headers):
    client.post("/premios/", json={"nome": "Prêmio Jabuti", "tipo": "livro"}, headers=auth_headers)
    resposta = client.put(
        "/premios/1",
        json={"descricao": "O mais tradicional prêmio literário do Brasil."},
        headers=auth_headers
    )
    assert resposta.status_code == 200
    assert resposta.json()["descricao"] == "O mais tradicional prêmio literário do Brasil."


def test_deletar_premio(client, auth_headers):
    client.post("/premios/", json={"nome": "Prêmio Jabuti", "tipo": "livro"}, headers=auth_headers)
    resposta = client.delete("/premios/1", headers=auth_headers)
    assert resposta.status_code == 204


def test_deletar_premio_inexistente(client, auth_headers):
    resposta = client.delete("/premios/999", headers=auth_headers)
    assert resposta.status_code == 404