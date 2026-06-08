# QA Documentation API

API de perguntas e respostas sobre documentos internos usando RAG (Retrieval-Augmented Generation).

O usuário envia uma pergunta via HTTP; o sistema busca os trechos mais relevantes num vector store (FAISS) e usa um LLM da OpenAI para gerar a resposta fundamentada nesses trechos.

---

## Stack

- **FastAPI** — framework HTTP
- **LangChain** — orquestração do pipeline RAG (LCEL)
- **OpenAI** — LLM (`gpt-4o-mini` por padrão) e embeddings
- **FAISS** — vector store local
- **Uvicorn** — ASGI server

---

## Estrutura do projeto

```
qa-documentation-api/
├── app.py                        # Entry point FastAPI
├── requirements.txt
│
├── api/routes/
│   └── ask.py                    # POST /ask
│
├── schemas/
│   └── ask_schema.py             # AskRequest / AskResponse
│
├── core/
│   └── config.py                 # Variáveis de ambiente
│
├── domain/services/
│   └── qa_service.py             # Orquestração de negócio
│
├── infra/
│   ├── embeddings/               # OpenAIEmbeddings
│   ├── llm/                      # ChatOpenAI
│   ├── rag/                      # Pipeline LCEL (create_retrieval_chain)
│   └── vectorstore/              # FAISS load / save
│
└── ingestion/
    ├── indexer.py                 # Script de ingestão de documentos
    ├── loaders/                   # TextLoader
    └── processors/                # RecursiveCharacterTextSplitter
```

---

## Pré-requisitos

- Python 3.12+
- Chave de API da OpenAI

---

## Configuração

1. Clone o repositório e crie o ambiente virtual:

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux / macOS
source .venv/bin/activate
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Crie o arquivo `.env` na raiz do projeto com base no exemplo:

```bash
cp .env.example .env
```

Edite o `.env` com sua chave:

```env
OPENAI_API_KEY="sua_chave_aqui"
MODEL_NAME="gpt-4o-mini"   # opcional — este é o padrão
```

---

## Indexando documentos

Antes de usar o endpoint `/ask`, é necessário indexar ao menos um documento para popular o vector store.

Coloque o arquivo de texto em `data/` e execute:

```bash
python -m ingestion.indexer
```

Por padrão o script lê `data/sample.txt`. Para indexar outro arquivo, altere o caminho na chamada `run_indexing()` em `ingestion/indexer.py`.

O vector store será salvo em `data/vectorstore/`.

---

## Executando a API

```bash
uvicorn app:app --reload
```

A API estará disponível em `http://localhost:8000`.

---

## Endpoints

### `GET /health`

Verifica se a API está no ar.

**Resposta:**
```json
{ "status": "ok" }
```

---

### `POST /ask`

Envia uma pergunta e recebe a resposta gerada pelo LLM com base nos documentos indexados.

**Body:**
```json
{
  "question": "Qual é a política de férias da empresa?"
}
```

**Resposta:**
```json
{
  "answer": "Conforme o documento, a política de férias prevê...",
  "sources": [
    { "source": "data/sample.txt" }
  ]
}
```

---

## Executando com Docker

```bash
docker build -t qa-documentation-api -f infra/Dockerfile .
docker run --env-file .env -p 8000:8000 qa-documentation-api
```

> O vector store precisa ser gerado antes de buildar a imagem, ou montado como volume:
>
> **Linux / macOS:**
> ```bash
> docker run --env-file .env -v $(pwd)/data:/app/data -p 8000:8000 qa-documentation-api
> ```
>
> **Windows (PowerShell):**
> ```powershell
> docker run --env-file .env -v ${PWD}/data:/app/data -p 8000:8000 qa-documentation-api
> ```

---

## Variáveis de ambiente

| Variável | Obrigatória | Padrão | Descrição |
|---|---|---|---|
| `OPENAI_API_KEY` | Sim | — | Chave de API da OpenAI |
| `MODEL_NAME` | Não | `gpt-4o-mini` | Modelo de LLM a ser usado |
