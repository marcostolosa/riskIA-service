import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

class RiskModel:
    def __init__(self):
        self.model = None
        self.feature_columns = None

    def train_model(self, csv_file: str = "data/training.csv"):
        df = pd.read_csv(csv_file)

        binary_cols = ['Exposição Pública', 'Dados Sensíveis', 'Histórico Incidentes',
                       'SAST Alto Risco', 'DAST Alto Risco', 'Aplicação MFA']
        
        df[binary_cols] = df[binary_cols].replace({"Sim": 1, "Não": 0})

        df = pd.get_dummies(df, columns=['Tipo de Aplicação'], prefix='TipoApp', drop_first=False)

        self.feature_columns = df.drop(columns=['Aprovado_AppSec']).columns

        X = df[self.feature_columns]
        y = df['Aprovado_AppSec']

        self.model = RandomForestClassifier(
            n_estimators=500,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2,
            class_weight="balanced",
            random_state=42
        )
        self.model.fit(X, y)

        y_pred = self.model.predict(X)
        print(classification_report(y, y_pred))

    def predict(self, features: dict):
        input_df = pd.DataFrame([features])

        binary_cols = ['exposicao_publica', 'dados_sensiveis', 'historico_incidentes',
                       'sast_alto_risco', 'dast_alto_risco', 'aplicacao_mfa']
        
        input_df[binary_cols] = input_df[binary_cols].replace({"Sim": 1, "Não": 0})

        input_df = pd.get_dummies(input_df, columns=['tipo_aplicacao'], prefix='TipoApp')
        for col in self.feature_columns:
            if col not in input_df.columns:
                input_df[col] = 0

        input_df = input_df[self.feature_columns]

        prediction = self.model.predict(input_df)[0]
        probas = self.model.predict_proba(input_df)[0]

        risco = 'alto' if probas[0] >= 0.7 else 'medio' if probas[0] >= 0.4 else 'baixo'

        return bool(prediction), risco

    def save_model(self, path="data/risk_model.pkl"):
        with open(path, "wb") as f:
            joblib.dump((self.model, self.feature_columns), f)

    def load_model(self, path="data/risk_model.pkl"):
        with open(path, "rb") as f:
            self.model, self.feature_columns = joblib.load(f)
