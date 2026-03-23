# 📧 Customer Support Agent

AI-powered customer support email agent using LangGraph, LangChain, and FastAPI. Classifies emails, generates responses with RAG, and escalates complex issues.

## ⚡ Quick Start (5 minutes)

```bash
# 1. Setup
python -m venv venv
venv\Scripts\activate  # Windows: or source venv/bin/activate on Mac/Linux
pip install -r requirements.txt

# 2. Configure
cp .env.example .env
# Edit .env and add: OPENAI_API_KEY=sk-...

# 3. Load knowledge base
python load_knowledge_base.py

# 4. Run
python main.py

# 5. Open in browser
http://localhost:8000
```

## ✨ Features

- 🤖 **Email Classification** — Intent, urgency, category via OpenAI
- 🔍 **RAG-based Responses** — Uses FAISS + knowledge base for context
- 📋 **Smart Escalation** — Routes complex/urgent emails to humans
- 🌐 **Web UI** — Test emails, view dashboard, explore APIs
- 📊 **Full API** — REST endpoints for integration
- 📧 **Email Integration** — SMTP sending + follow-up scheduling

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| LLM | OpenAI (GPT-4) |
| Framework | LangGraph + LangChain |
| Vector Store | FAISS (CPU) |
| Web API | FastAPI + Uvicorn |
| Config | Pydantic Settings |
| Scheduling | APScheduler |
| Logging | Loguru |

## 📁 Structure

```
src/
├── api/         # FastAPI routes (web UI + API endpoints)
├── graph/       # LangGraph state machine
├── nodes/       # Processing nodes (classifier, responder, etc.)
├── services/    # Email & knowledge base services
├── prompts/     # LLM prompt templates
├── schemas/     # Pydantic data models
├── core/        # Config & logging
└── utils/       # Helpers

data_or_knowledge_graph/
├── knowledge_base/    # FAQ documents (TXT format)
└── faiss_index/       # Vector store (auto-created)
```

## 🌐 Web UI

| Page | URL | Purpose |
|------|-----|---------|
| **Test Email** | http://localhost:8000/ | Submit & test emails with quick examples |
| **Dashboard** | http://localhost:8000/dashboard | View all processed emails & stats |
| **API Docs** | http://localhost:8000/api-docs | Interactive API documentation |

## 📡 API Endpoints

```bash
GET  /health              # Health check
POST /api/emails          # Submit email
GET  /api/emails/{id}     # Get email status
GET  /api/emails-list     # List all emails
```

## 🔧 Configuration

Set in `.env`:
```env
OPENAI_API_KEY=sk-...           # Required
OPENAI_MODEL=gpt-4              # LLM model
API_PORT=8000                   # Server port
LOG_LEVEL=INFO                  # Logging level
SMTP_USERNAME=your@gmail.com    # Optional: for real email
SMTP_PASSWORD=app_password      # Optional: Google App Password
```

## 📚 Documentation

- **Setup Guide** → [QUICKSTART.md](UI_QUICKSTART.md)
- **UI Guide** → [UI_GUIDE.md](UI_GUIDE.md)
- **FAISS Setup** → [FAISS_GUIDE.md](FAISS_GUIDE.md)
- **API Reference** → Visit `/api-docs` when app is running

## 🚀 Workflow

```
Email Received
    ↓
Classify (intent, urgency, category)
    ↓
Retrieve docs from FAISS knowledge base
    ↓
Generate response via OpenAI + context
    ↓
Route: Escalate (urgent) or Send (auto-reply)?
    ↓
Send email + schedule follow-up
```

## ✅ Sample Email Processing

```
Input: "Unable to reset my password"
  ↓
Classification: intent=question, urgency=high, category=account
  ↓
Retrieved: Password reset FAQ from knowledge base
  ↓
Response: "Click Forgot Password on login page..."
  ↓
Status: SENT ✓
```


