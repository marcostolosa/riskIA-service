# AI Risk Analysis Service

O **AI Risk Analysis Service** é uma API desenvolvida em **FastAPI** que utiliza **Machine Learning** para analisar e classificar o risco de aplicações digitais. O serviço recebe informações sobre a aplicação, avalia sua segurança e fornece uma classificação baseada em critérios pré-definidos de **AppSec (Application Security)**. O modelo de decisão utiliza um **DecisionTreeClassifier** para determinar se a aplicação deve ser aprovada e qual seu nível de risco (baixo, médio ou alto).

## 📌 Tecnologias Utilizadas
- **Python**
- **FastAPI** (para a API REST)
- **Scikit-Learn** (para aprendizado de máquina)
- **Pandas** (para manipulação de dados)
- **Pydantic** (para validação de dados)

## 🚀 Instalação e Execução

### 1️⃣ Clonar o repositório
```bash
git clone https://github.com/seu_usuario/seu_repositorio.git
cd seu_repositorio
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

### 4️⃣ Executar o servidor
```bash
uvicorn main:app --reload
```

A API estará disponível em `http://127.0.0.1:8000`.

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

## 📊 Treinamento do Modelo
O modelo é treinado automaticamente ao iniciar a API. Ele utiliza um dataset localizado em `data/training_data.csv`, que deve conter as seguintes colunas:

- **Tipo de Aplicação**: Web, Mobile ou API
- **Exposição Pública**: Sim/Não
- **Dados Sensíveis?**: Sim/Não
- **Histórico de Incidentes?**: Sim/Não
- **Resultado do Scan SAST (alto risco)?**: Sim/Não
- **Resultado do Scan DAST (alto risco)?**: Sim/Não
- **Aplicação com MFA?**: Sim/Não
- **Aprovado_AppSec**: Sim/Não (Variável alvo do modelo)

### 🔹 Processo de Treinamento
1. **Carregamento e Pré-processamento dos Dados**:
   - O dataset é carregado e tratado com a biblioteca `pandas`.
   - As colunas categóricas que possuem valores `Sim/Não` são convertidas para valores numéricos (1 para "Sim", 0 para "Não").
   - A coluna `Tipo de Aplicação` é transformada em variáveis dummies (`TipoApp_Web`, `TipoApp_Mobile`, `TipoApp_API`).
2. **Separação de Features e Variável Alvo**:
   - A variável `Aprovado_AppSec` é separada como **target (y)**.
   - As demais colunas são utilizadas como **features (X)**.
3. **Treinamento do Modelo**:
   - Utiliza-se um **DecisionTreeClassifier** com `max_depth=4` para encontrar padrões e evitar overfitting.
   - O modelo treinado fica armazenado em memória para futuras previsões.

Caso o dataset de treinamento não esteja presente ou o modelo não seja carregado corretamente, a API retornará um erro.

## 📈 Precisão e Explicabilidade do Modelo
O uso de uma **Árvore de Decisão** facilita a interpretação dos resultados, pois permite visualizar os critérios que levaram a uma determinada classificação de risco. O modelo pode ser ajustado conforme necessário para aumentar a precisão e otimização.

## 🛠 Como Contribuir
1. Faça um fork do projeto
2. Crie uma branch (`git checkout -b feature-nova`)
3. Faça commit das suas alterações (`git commit -m 'Adiciona nova feature'`)
4. Envie para o repositório (`git push origin feature-nova`)
5. Abra um Pull Request

## 📄 Licença
Este projeto está sob a licença MIT. Sinta-se à vontade para usá-lo e modificá-lo conforme necessário!

