# LangGraph Customer Support Email Agent

A Python-based customer support email agent built with LangGraph, LangChain, and FastAPI. This agent intelligently classifies, responds to, and escalates customer emails using OpenAI's language models.

## Features (Planned)

- **Email Classification**: Automatically categorize incoming emails by intent and urgency
- **Intelligent Response Generation**: Generate contextual responses using RAG (Retrieval-Augmented Generation)
- **Human Escalation**: Route complex issues to human support team members
- **Knowledge Base Integration**: Leverage ChromaDB for efficient document retrieval
- **REST API**: FastAPI-based endpoints for email submission and status tracking

## Tech Stack

- **Python 3.12+**
- **LangGraph** — Agentic workflow orchestration
- **LangChain** — LLM framework and tooling
- **FastAPI** — Web framework
- **OpenAI API** — LLM backbone
- **ChromaDB** — Vector store for RAG
- **Pydantic** — Data validation
- **Loguru** — Structured logging

## Project Structure

```
support-agent-using-claude/
├── src/
│   ├── api/                  # FastAPI routes & dependencies
│   ├── graph/                # LangGraph state machine definitions
│   ├── nodes/                # Graph node implementations
│   ├── services/             # Business logic (email, knowledge base)
│   ├── prompts/              # LangChain prompt templates
│   ├── schemas/              # Pydantic models
│   ├── core/                 # Config, logging setup
│   └── utils/                # Helper utilities
├── data_or_knowledge_graph/  # Knowledge base & sample data
├── tests/                    # Test suite (pytest)
├── main.py                   # FastAPI app entry point
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variables template
└── README.md                 # This file
```

## Setup

### Prerequisites

- Python 3.12+
- pip

### Installation

1. Clone the repository:
   ```bash
   git clone <repo_url>
   cd support-agent-using-claude
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key and other config
   ```

### Running the Application

Start the FastAPI server:

```bash
python main.py
```

The API will be available at `http://localhost:8000`.

**Health Check:**
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "ok"
}
```

### Running Tests

```bash
pytest tests/
```

For verbose output:
```bash
pytest tests/ -v
```

## API Endpoints (Planned)

- `GET /health` — Health check
- `POST /api/emails` — Submit an email for processing
- `GET /api/emails/{email_id}` — Retrieve email processing status

## Configuration

All configuration is managed via environment variables in `.env`. Key variables:

| Variable | Description | Example |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key | `sk-...` |
| `OPENAI_MODEL` | OpenAI model to use | `gpt-4` |
| `API_PORT` | FastAPI port | `8000` |
| `LOG_LEVEL` | Logging level | `INFO` |

See `.env.example` for all available options.

## Development

### Code Structure Overview

- **`src/graph/agent_graph.py`** — Main LangGraph StateGraph definition
- **`src/nodes/`** — Individual node implementations (classifier, responder, escalation)
- **`src/api/routes/email.py`** — Email submission & retrieval endpoints
- **`src/services/`** — Email & knowledge base service abstractions
- **`src/core/config.py`** — Application configuration via pydantic-settings

### Adding New Features

1. Create node implementations in `src/nodes/`
2. Register nodes in `src/graph/agent_graph.py`
3. Add API endpoints in `src/api/routes/`
4. Add tests in `tests/`

## Next Steps

1. Implement core LangGraph nodes (classifier, responder, escalation)
2. Set up OpenAI integration
3. Implement email service layer
4. Add knowledge base ingestion
5. Build API endpoints
6. Write integration tests

## Contributing

TBD

## License

TBD

## Support

For questions or issues, please open a GitHub issue or contact the development team.
