import pandas as pd
from sklearn.tree import DecisionTreeClassifier

class RiskModel:
    def __init__(self):
        self.model = None

    def train_model(self, csv_file: str = "data/training_data.csv"):
        """
        Treina (ou re-treina) o modelo de decisão de risco
        a partir de um CSV.
        O CSV deve conter as colunas:
          - 'Tipo de Aplicação' (Web/Mobile/API)
          - 'Exposição Pública' (Sim/Não)
          - 'Dados Sensíveis?' (Sim/Não)
          - 'Histórico de Incidentes?' (Sim/Não)
          - 'Resultado do Scan SAST (alto risco)?' (Sim/Não)
          - 'Resultado do Scan DAST (alto risco)?' (Sim/Não)
          - 'Aplicação com MFA?' (Sim/Não)
          - 'Aprovado_AppSec' (Sim/Não) -> coluna alvo
        """
        df = pd.read_csv(csv_file)

        # Mapa Sim/Não -> 1/0
        mapa_binario = {'Sim': 1, 'Não': 0}

        df['Exposicao_Publica'] = df['Exposição Pública'].map(mapa_binario)
        df['Dados_Sensiveis'] = df['Dados Sensíveis?'].map(mapa_binario)
        df['Historico_Incidentes'] = df['Histórico de Incidentes?'].map(mapa_binario)
        df['SAST_Alto_Risco'] = df['Resultado do Scan SAST (alto risco)?'].map(mapa_binario)
        df['DAST_Alto_Risco'] = df['Resultado do Scan DAST (alto risco)?'].map(mapa_binario)
        df['Aplicacao_MFA'] = df['Aplicação com MFA?'].map(mapa_binario)

        # One-Hot Encoding para 'Tipo de Aplicação'
        df = pd.get_dummies(df, columns=['Tipo de Aplicação'],
                            prefix='TipoApp', drop_first=False)

        # Converte "Sim"/"Não" alvo em 1/0
        df['Aprovado_AppSec'] = df['Aprovado_AppSec'].map(mapa_binario)

        # Remove colunas textuais originais (desnecessárias agora)
        df.drop([
            'Exposição Pública',
            'Dados Sensíveis?',
            'Histórico de Incidentes?',
            'Resultado do Scan SAST (alto risco)?',
            'Resultado do Scan DAST (alto risco)?',
            'Aplicação com MFA?'
        ], axis=1, inplace=True)

        # Separa features e alvo
        X = df.drop('Aprovado_AppSec', axis=1)
        y = df['Aprovado_AppSec']

        # Treina a árvore de decisão
        model = DecisionTreeClassifier(max_depth=7, random_state=42)
        model.fit(X, y)
        self.model = model

    def predict(self, features: dict):
        """
        Recebe um dicionário com strings (Sim/Não, Web/Mobile/API)
        Converte para numérico e faz previsão (True/False) e
        nível de risco (baixo, medio, alto).
        """
        if not self.model:
            raise ValueError("Modelo não foi carregado ou treinado.")

        # 1. Converter as entradas 'features' em DataFrame com 0/1 e one-hot
        df_input = self._transform_input(features)
        prediction = self.model.predict(df_input)[0]  # 0 ou 1

        # Obter probabilidades para classificar risco
        probas = self.model.predict_proba(df_input)[0]
        # probas[0] => probabilidade de ser '0' (não aprovado)
        # probas[1] => probabilidade de ser '1' (aprovado)

        prob_reprovado = probas[0]
        prob_aprovado = probas[1]

        # Exemplo de classificação do "nível de risco"
        # quanto maior a prob_reprovado, mais alto o risco
        if prob_reprovado >= 0.7:
            risco_label = "alto"
        elif 0.4 <= prob_reprovado < 0.7:
            risco_label = "medio"
        else:
            risco_label = "baixo"

        return bool(prediction), risco_label

    def _transform_input(self, features: dict) -> pd.DataFrame:
        """
        Converte as entradas textuais ('Sim'/'Não', 'Web'/'API'/'Mobile')
        para as colunas numéricas e one-hot do modelo.
        """
        # Mapa Sim/Não
        mapa_binario = {'Sim': 1, 'Não': 0}

        # Converter cada entrada usando o mapa
        exposicao_publica = mapa_binario.get(features.get("exposicao_publica"), 0)
        dados_sensiveis = mapa_binario.get(features.get("dados_sensiveis"), 0)
        historico_incidentes = mapa_binario.get(features.get("historico_incidentes"), 0)
        sast_alto_risco = mapa_binario.get(features.get("sast_alto_risco"), 0)
        dast_alto_risco = mapa_binario.get(features.get("dast_alto_risco"), 0)
        aplicacao_mfa = mapa_binario.get(features.get("aplicacao_mfa"), 0)

        tipo_aplicacao = features.get("tipo_aplicacao", "Web")  # default "Web"

        # Cria as colunas one-hot manualmente de acordo com a lógica do treinamento
        tipo_app_api = 1 if tipo_aplicacao == "API" else 0
        tipo_app_mobile = 1 if tipo_aplicacao == "Mobile" else 0
        tipo_app_web = 1 if tipo_aplicacao == "Web" else 0

        # Monta o dicionário com as colunas
        row = {
            "Exposicao_Publica": exposicao_publica,
            "Dados_Sensiveis": dados_sensiveis,
            "Historico_Incidentes": historico_incidentes,
            "SAST_Alto_Risco": sast_alto_risco,
            "DAST_Alto_Risco": dast_alto_risco,
            "Aplicacao_MFA": aplicacao_mfa,
            "TipoApp_API": tipo_app_api,
            "TipoApp_Mobile": tipo_app_mobile,
            "TipoApp_Web": tipo_app_web
        }

        # Cria o DataFrame e força a mesma ordem de colunas que foi usada no treinamento
        df_input = pd.DataFrame([row])
        col_order = [
            "Exposicao_Publica",
            "Dados_Sensiveis",
            "Historico_Incidentes",
            "SAST_Alto_Risco",
            "DAST_Alto_Risco",
            "Aplicacao_MFA",
            "TipoApp_API",
            "TipoApp_Mobile",
            "TipoApp_Web"
        ]
        return df_input[col_order]
