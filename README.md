# AI Risk Analysis Service

O **AI Risk Analysis Service** é uma API desenvolvida em **FastAPI** que utiliza **Machine Learning** para analisar e classificar o risco de aplicações digitais. O serviço recebe informações sobre a aplicação, avalia sua segurança e fornece uma classificação baseada em critérios pré-definidos de **AppSec (Application Security)**. O modelo de decisão utiliza um **RandomForestClassifier** para determinar se a aplicação deve ser aprovada e qual seu nível de risco (baixo, médio ou alto).

## 📌 Tecnologias Utilizadas
- **Python**
- **FastAPI** (para a API REST)
- **Scikit-Learn** (para aprendizado de máquina)
- **Pandas** (para manipulação de dados)
- **Pydantic** (para validação de dados)

## 🚀 Instalação e Execução

### 1️⃣ Clonar o repositório
```bash
git clone https://github.com/marcostolosa/riskIA-service.git
cd riskIA-service/
```

### 2️⃣ Criar um ambiente virtual e ativá-lo
```bash
python -m venv venv
source venv/bin/activate  # No Windows, use `venv\Scripts\activate`
```

### 3️⃣ Instalar as dependências
```bash
pip install -r requirements.txt
```

### 4️⃣ Executar a API
```bash
uvicorn main:app --reload
```

## 📚 Modelo de Machine Learning
Utilizamos um modelo RandomForestClassifier com as seguintes configurações:

- **n_estimators=500**: número de árvores no modelo.
- **max_depth=10**: controla a complexidade das árvores para evitar overfitting.
- **min_samples_split=5**: número mínimo de amostras para dividir um nó.
- **min_samples_leaf=2**: número mínimo de amostras nas folhas finais.
- **class_weight="balanced"**: ajusta automaticamente o peso das classes.
- **random_state=42**: garante reprodutibilidade.

O modelo é treinado automaticamente no início da API e salvo em arquivo usando `joblib`.

## 📈 Precisão e Explicabilidade do Modelo
A utilização do **Random Forest** aumenta a precisão e a robustez contra overfitting. Além disso, permite analisar a importância das variáveis para melhor explicabilidade.

## 📚 Endpoints

### ✅ Verificar Status da API
**GET /**
```json
{
  "message": "AI Risk Analysis Service is running!"
}
```

### 🔍 Predição de Risco
**POST /predict**

Este endpoint recebe informações sobre uma aplicação e retorna uma análise de risco baseada no modelo treinado.

#### 🔹 Parâmetros de Entrada (JSON):
```json
{
  "tipo_aplicacao": "Web",
  "exposicao_publica": "Sim",
  "dados_sensiveis": "Sim",
  "historico_incidentes": "Não",
  "sast_alto_risco": "Não",
  "dast_alto_risco": "Sim",
  "aplicacao_mfa": "Sim"
}
```

#### 🔹 Resposta Esperada:
```json
{
  "aprovado_appsec": true,
  "risco": "baixo"
}
```

## 🧪 Testes Automatizados
Utilizamos **pytest** para testes automatizados.

### 🔹 Executando os testes
```bash
pip install pytest
pytest
```

## 🛠 Como Contribuir
1. Faça um fork do projeto
2. Crie uma branch (`git checkout -b feature-nova`)
3. Faça commit das suas alterações (`git commit -m 'Adiciona nova feature'`)
4. Envie para o repositório (`git push origin feature-nova`)
5. Abra um Pull Request

## 📄 Licença
Este projeto está sob a licença MIT. Sinta-se à vontade para usá-lo e modificá-lo conforme necessário!

