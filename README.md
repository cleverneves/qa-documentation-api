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
│   └── ask_schema.py             # AskRequest / AskResponse / SourceDocument
│
├── core/
│   └── config.py                 # Variáveis de ambiente (OPENAI_API_KEY, MODEL_NAME)
│
├── domain/services/
│   └── qa_service.py             # Orquestração de negócio
│
├── infra/
│   ├── providers.py              # ChatOpenAI e OpenAIEmbeddings
│   ├── rag/                      # Pipeline LCEL (create_retrieval_chain)
│   └── vectorstore/              # FAISS load / save
│
├── ingestion/
│   ├── indexer.py                # Script de ingestão de documentos
│   └── loaders/                  # Suporte a .txt, .md, .pdf, .docx
│
└── tests/                        # Suite de testes (pytest)
```

---

## Pré-requisitos

- Python 3.12+
- Chave de API da OpenAI

---

## Configuração

1. Clone o repositório e crie o ambiente virtual:

Para Windows:
```bash
git clone https://github.com/cleverneves/qa-documentation-api.git
# ou 
git clone git@github.com:cleverneves/qa-documentation-api.git

python -m venv .venv

.venv\Scripts\activate
```

Para Linux / macOS:
```bash
git clone https://github.com/cleverneves/qa-documentation-api.git
# ou
git clone git@github.com:cleverneves/qa-documentation-api.git

python -m venv .venv

source .venv/bin/activate
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Crie o arquivo `.env` na raiz do projeto com base no exemplo:

**Linux / macOS:**
```bash
cp infra/.env.example .env
```

**Windows (PowerShell):**
```powershell
copy infra\.env.example .env
```

Edite o `.env` com sua chave:

```env
OPENAI_API_KEY="sua_chave_aqui"
MODEL_NAME="gpt-4o-mini"   # opcional — este é o padrão
```

---

## Indexando documentos

Antes de usar o endpoint `/ask`, é necessário indexar ao menos um documento para popular o vector store.

Um documento de exemplo já está disponível em `data/sample.txt`. Para indexá-lo:

```bash
python -m ingestion.indexer
```

Para indexar outro arquivo, use o argumento `--file`:

```bash
python -m ingestion.indexer --file data/meu-documento.pdf
```

**Formatos suportados:** `.txt`, `.md`, `.pdf`, `.docx`

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
    { "source": "data/sample.txt", "page": null }
  ]
}
```

O campo `page` é preenchido automaticamente para arquivos PDF (número da página) e `null` para demais formatos.

---

## Testes

```bash
pytest tests/ -v
```

Os testes não dependem de chave de API nem de vector store — todo acesso à OpenAI e ao FAISS é mockado.

---

## Executando com Docker Compose

### 1. Indexar os documentos

O vector store precisa ser populado antes de subir a API. Rode o serviço de ingestão:

```bash
docker compose --profile tools run --rm indexer
```

Para indexar outro arquivo:

```bash
docker compose --profile tools run --rm indexer python -m ingestion.indexer --file data/meu-doc.pdf
```

### 2. Subir a API

```bash
docker compose up api
```

A API estará disponível em `http://localhost:8000`.

---

### Executando com Docker (sem Compose)

```bash
docker build -t qa-documentation-api -f infra/Dockerfile .
docker run --env-file .env -p 8000:8000 qa-documentation-api
```

---

## Variáveis de ambiente

| Variável | Obrigatória | Padrão | Descrição |
|---|---|---|---|
| `OPENAI_API_KEY` | Sim | — | Chave de API da OpenAI |
| `MODEL_NAME` | Não | `gpt-4o-mini` | Modelo de LLM a ser usado |
