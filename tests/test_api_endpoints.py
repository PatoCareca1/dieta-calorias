import pytest
from datetime import date

def test_full_crud_flow(client):
    # 1) Cria usuário
    resp = client.post("/usuarios/", json={
        "nome": "Teste Integração",
        "email": "integ@teste.com",
        "senha": "senha123",
        "peso": 70,
        "altura": 1.75,
        "meta_calorica_diaria": 2000
    })
    assert resp.status_code == 201
    user = resp.json()
    user_id = user["id_usuario"]

    # 2) Cria alimento
    resp = client.post("/alimentos/", json={
        "nome": "Batata",
        "calorias_por_100g": 77,
        "proteinas": 2.0,
        "carboidratos": 17.0,
        "gorduras": 0.1
    })
    assert resp.status_code == 201
    alimento = resp.json()
    alim_id = alimento["id_alimento"]

    # 3) Cria refeição
    today = date.today().isoformat()
    resp = client.post("/refeicoes/", json={
        "user_id": user_id,
        "data": today,
        "tipo_refeicao": "Almoço"
    })
    assert resp.status_code == 201
    refeicao = resp.json()
    ref_id = refeicao["id_refeicao"]

    # 4) Cria item de refeição
    resp = client.post("/itens-refeicao/", json={
        "id_refeicao": ref_id,
        "id_alimento": alim_id,
        "quantidade_em_gramas": 150
    })
    assert resp.status_code == 201
    item = resp.json()
    item_id = item["id_item"]
    assert item["quantidade_em_gramas"] == 150

    # 5) Busca resumo de calorias do dia
    resp = client.get(f"/calorias/resumo/{user_id}")
    assert resp.status_code == 200
    resumo = resp.json()
    # 150g de batata → 150 * 77 / 100 = 115.5 kcal
    assert pytest.approx(resumo["total_calorias"], rel=1e-3) == 115.5
    assert resumo["status"] == "abaixo"

    # 6) Limpeza: delete item, refeição, alimento, usuário
    assert client.delete(f"/itens-refeicao/{item_id}").status_code == 204
    assert client.delete(f"/refeicoes/{ref_id}").status_code == 204
    assert client.delete(f"/alimentos/{alim_id}").status_code == 204
    assert client.delete(f"/usuarios/{user_id}").status_code == 204
