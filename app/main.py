from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from .schemas import RiskInput, RiskOutput
from .model import RiskModel

app = FastAPI(
    title="AI Risk Analysis Service",
    description="Serviço de análise de risco baseado em IA (AppSec).",
    version="1.0.0"
)

risk_model = RiskModel()

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        risk_model.train_model("data/training_data.csv")
        print("Modelo treinado/carregado com sucesso!")
    except Exception as e:
        print(f"Erro ao treinar/carregar o modelo: {e}")
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
def root():
    return {"message": "AI Risk Analysis Service is running!"}

@app.post("/predict", response_model=RiskOutput)
def predict_risk(input_data: RiskInput):
    """
    Recebe dados de risco e retorna se a aplicação deve ou não ser aprovada
    e qual o nível de risco (baixo, medio, alto).
    """
    try:
        aprovado, risco = risk_model.predict(input_data.model_dump())
        return RiskOutput(aprovado_appsec=aprovado, risco=risco)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
