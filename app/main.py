from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from pydantic import BaseModel
import joblib
import os
from app.model import RiskModel

risk_model = RiskModel()
MODEL_PATH = "data/risk_model.pkl"

@asynccontextmanager
async def lifespan(app: FastAPI):
    if os.path.exists(MODEL_PATH):
        risk_model.load_model(MODEL_PATH)
        print("✅ Modelo carregado com sucesso!")
    else:
        risk_model.train_model("data/training_data.csv")
        risk_model.save_model(MODEL_PATH)
        print("✅ Modelo treinado e salvo com sucesso!")
    yield

app = FastAPI(
    title="AI Risk Analysis Service",
    description="Serviço de análise de risco baseado em IA (AppSec).",
    version="2.0.0",
    lifespan=lifespan
)

@app.get("/")
def root():
    return {"message": "AI Risk Analysis Service is running!"}

@app.post("/predict", response_model=RiskOutput)
def predict_risk(input_data: RiskInput):
    try:
        aprovado, risco = risk_model.predict(input_data.model_dump())
        return RiskOutput(aprovado_appsec=aprovado, risco=risco)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=f"Erro no modelo: {ve}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {e}")
