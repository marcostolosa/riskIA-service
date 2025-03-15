import pytest
from fastapi.testclient import TestClient
from app.main import app, risk_model

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "AI Risk Analysis Service is running!"}

def test_train_model():
    """ Garante que o modelo seja treinado antes dos testes de predição. """
    try:
        risk_model.train_model("data/training_data.csv")
    except Exception as e:
        pytest.fail(f"Erro ao treinar o modelo: {e}")

def test_predict_risk_valid():
    test_data = {
        "tipo_aplicacao": "Web",
        "exposicao_publica": "Sim",
        "dados_sensiveis": "Sim",
        "historico_incidentes": "Não",
        "sast_alto_risco": "Não",
        "dast_alto_risco": "Sim",
        "aplicacao_mfa": "Sim"
    }
    response = client.post("/predict", json=test_data)
    assert response.status_code == 200
    assert "aprovado_appsec" in response.json()
    assert "risco" in response.json()

def test_predict_risk_invalid():
    invalid_data = {"tipo_aplicacao": "Desktop"}  # Faltando vários campos obrigatórios
    response = client.post("/predict", json=invalid_data)
    assert response.status_code == 422  # FastAPI retorna 422 para erros de validação Pydantic
