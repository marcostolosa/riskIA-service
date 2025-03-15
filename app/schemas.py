from pydantic import BaseModel

class RiskInput(BaseModel):
    tipo_aplicacao: str                 # Ex: "Web", "Mobile", "API"
    exposicao_publica: str              # "Sim" ou "Não"
    dados_sensiveis: str                # "Sim" ou "Não"
    historico_incidentes: str           # "Sim" ou "Não"
    sast_alto_risco: str                # "Sim" ou "Não"
    dast_alto_risco: str                # "Sim" ou "Não"
    aplicacao_mfa: str                  # "Sim" ou "Não"

class RiskOutput(BaseModel):
    aprovado_appsec: bool
    risco: str  # "baixo", "médio" ou "alto"
