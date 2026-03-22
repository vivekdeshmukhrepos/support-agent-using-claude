# FAISS Knowledge Base Implementation Guide

## Overview

This project now uses **FAISS (Facebook AI Similarity Search)** as the vector store for the knowledge base instead of ChromaDB. FAISS is a lightweight, fast similarity search library that's perfect for RAG (Retrieval-Augmented Generation) workflows.

## What is FAISS?

- **Fast**: Uses optimized algorithms for vector similarity search
- **Lightweight**: No external dependencies like a database server
- **Simple**: Easy to integrate with LangChain
- **Scalable**: Can handle millions of vectors efficiently
- **Local**: Stores index on disk for persistence

## Architecture

```
Documents (TXT files)
       ↓
TextLoader + RecursiveCharacterTextSplitter
       ↓
Chunks (500 chars, 50 char overlap)
       ↓
OpenAI Embeddings (text-embedding-3-small)
       ↓
FAISS Index (stored on disk)
       ↓
Similarity Search → Top-K Results
```

## Sample Documents

Four sample knowledge base documents have been created:

1. **account_help.txt** - Account management, password resets, 2FA, security
2. **billing_faq.txt** - Billing cycles, payment methods, invoices, refunds
3. **technical_support.txt** - Error codes, API integration, troubleshooting
4. **general_faq.txt** - General questions, features, compliance, data export

Each document contains realistic customer support information that will be retrieved when customers ask related questions.

## Quick Start

### 1. Update Requirements
```bash
pip install -r requirements.txt
# This includes faiss-cpu (CPU version)
# Use: pip install faiss-gpu for GPU acceleration if available
```

### 2. Load Knowledge Base

The knowledge base needs to be loaded once to create the FAISS index:

```bash
python load_knowledge_base.py
```

This script will:
- Read all `.txt` files from `data_or_knowledge_graph/knowledge_base/`
- Split them into 500-character chunks
- Generate embeddings using OpenAI's `text-embedding-3-small`
- Create a FAISS index and save it to `data_or_knowledge_graph/faiss_index/`

**Output:**
```
INFO:     Loading knowledge base from ./data_or_knowledge_graph/knowledge_base
INFO:     Found 4 document files
INFO:     Loaded 4 documents total
INFO:     Split into 47 chunks
INFO:     FAISS index saved to ./data_or_knowledge_graph/faiss_index
```

### 3. Run the Application

```bash
python main.py
```

The app will start on `http://localhost:8000`

### 4. Submit Test Emails

```bash
curl -X POST http://localhost:8000/api/emails \
  -H "Content-Type: application/json" \
  -d '{
    "sender": "customer@example.com",
    "recipient": "support@company.com",
    "subject": "How do I reset my password?",
    "body": "I forgot my password and need to regain access to my account"
  }'
```

## How FAISS Works in the Pipeline

### Email Processing Flow

```
1. Email Received
   ↓
2. Classify Email
   - Intent: question, complaint, request, etc.
   - Urgency: low, medium, high, critical
   - Category: billing, technical, account, etc.
   ↓
3. Retrieve from FAISS Knowledge Base
   - Query: "{subject} {body}"
   - Embedding: Convert query to vector
   - Search: Find top-5 most similar chunks
   - Return: List of relevant document snippets
   ↓
4. Generate Response
   - Use LLM with prompt template
   - Include retrieved documents as context
   - Generate draft response
   ↓
5. Route Decision
   - If urgent → Escalate to human
   - If not urgent → Send auto-reply
   ↓
6. Schedule Follow-up
   - Based on urgency level
   - 2h for critical, 24h for high, etc.
```

## Key Files

### Knowledge Service
**File:** `src/services/knowledge_service.py`

Main class: `KnowledgeService`

Key methods:
- `load_knowledge_base(path)` - Load documents and create FAISS index
- `retrieve_relevant_docs(query, top_k=5)` - Search FAISS for similar documents
- `get_vectorstore_stats()` - Get index statistics

Example usage:
```python
from src.services.knowledge_service import KnowledgeService
from src.core.config import Settings

settings = Settings()
service = KnowledgeService(settings)

# Load documents
await service.load_knowledge_base()

# Retrieve documents for a query
docs = await service.retrieve_relevant_docs(
    query="How do I reset my password?",
    top_k=5
)

# Get stats
stats = service.get_vectorstore_stats()
print(f"Total vectors: {stats['total_vectors']}")
```

### Knowledge Retriever Node
**File:** `src/nodes/knowledge_retriever.py`

This is the node in the LangGraph pipeline that retrieves from FAISS:

```python
from src.nodes.knowledge_retriever import make_retriever

# In agent_graph.py
retriever = make_retriever(settings)
graph.add_node("knowledge_retriever", retriever)
```

## Customization

### Add More Documents

1. Create new `.txt` files in `data_or_knowledge_graph/knowledge_base/`
2. Run `python load_knowledge_base.py` again to reindex
3. The script will add new documents to the existing FAISS index

Example document structure:
```
TITLE OF SECTION

1. Subsection One
Description and details...

2. Subsection Two
More information...
```

### Adjust Chunk Size

In `src/services/knowledge_service.py`:
```python
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,        # Characters per chunk (increase for longer context)
    chunk_overlap=50,      # Overlap for context continuity
    separators=["\n\n", "\n", ".", " ", ""],  # How to split
)
```

### Adjust Relevance Threshold

In `src/services/knowledge_service.py`:
```python
if score < 1.5:  # Distance threshold (lower = more similar)
    doc_contents.append(doc.page_content)
```

Lower threshold = only very similar documents; Higher threshold = more lenient.

### Change Embedding Model

In `src/services/knowledge_service.py`:
```python
self.embeddings = OpenAIEmbeddings(
    api_key=self.settings.openai_api_key,
    model="text-embedding-3-large",  # Options: small, large
)
```

## Testing

### Test 1: Load Knowledge Base
```bash
python load_knowledge_base.py
```

### Test 2: Test Retrieval with Sample Queries
The `load_knowledge_base.py` script includes test queries:
- "How do I reset my password?"
- "What payment methods do you accept?"
- "I'm getting a 500 error"
- etc.

### Test 3: Full Workflow
```bash
python test_full_workflow.py
```

This comprehensive test:
1. Loads the knowledge base
2. Processes 3 sample emails through the full pipeline
3. Shows classification, retrieved documents, and generated responses

**Output example:**
```
Processing Email: Unable to reset my password
Email ID: email_abc123

📊 CLASSIFICATION RESULTS:
  Intent: question
  Urgency: high
  Category: account
  Confidence: 0.92

📚 RETRIEVED DOCUMENTS:
  [1] If you forgot your password, click on "Forgot Password" on the login page...
  [2] New accounts need to be verified before use...

💬 GENERATED RESPONSE:
  Hello! I understand you're having trouble resetting your password. Let me help...

✅ FINAL STATUS:
  Status: sent
  Escalated: false
```

### Test 4: API Test
```bash
# Start the app
python main.py

# In another terminal, submit an email
EMAIL_ID=$(curl -s -X POST http://localhost:8000/api/emails \
  -H "Content-Type: application/json" \
  -d '{
    "sender": "test@example.com",
    "recipient": "support@company.com",
    "subject": "Test subject",
    "body": "Test body"
  }' | jq -r '.email_id')

# Check status
curl http://localhost:8000/api/emails/$EMAIL_ID | jq .
```

## Troubleshooting

### Issue: OPENAI_API_KEY not found
**Solution:** Set the environment variable in `.env`:
```
OPENAI_API_KEY=sk-your-actual-key-here
```

### Issue: No documents found when loading
**Solution:** Ensure `.txt` files are in `data_or_knowledge_graph/knowledge_base/`:
```bash
ls data_or_knowledge_graph/knowledge_base/
# Should show: account_help.txt, billing_faq.txt, etc.
```

### Issue: FAISS index not loading
**Solution:** Delete the index and reload:
```bash
rm -rf data_or_knowledge_graph/faiss_index/
python load_knowledge_base.py
```

### Issue: Poor retrieval results
**Solution:**
1. Check chunk size (too small = lost context, too large = noise)
2. Adjust relevance threshold
3. Ensure query is similar to document content
4. Add more diverse documents to the knowledge base

## Performance Notes

- **First load:** ~5-10 seconds (depends on document size and OpenAI API latency)
- **Subsequent loads:** <1 second (loads from disk cache)
- **Search latency:** <10ms (FAISS is very fast)
- **Index size:** ~2-5MB per 1000 vectors

## FAISS vs ChromaDB Comparison

| Aspect | FAISS | ChromaDB |
|--------|-------|----------|
| Setup | Simple | Requires more setup |
| Persistence | Disk file | Disk + metadata |
| Speed | Very fast | Fast |
| Dependencies | Few | More dependencies |
| Memory | Low | Moderate |
| Suitable for | Simple to medium | Medium to large |

FAISS is perfect for this project because:
- No database server required
- Fast similarity search
- Easy to persist and reload
- Good for up to millions of vectors

## Next Steps

1. ✅ Load knowledge base with sample documents
2. ✅ Test retrieval with sample queries
3. ✅ Process sample emails through full pipeline
4. 📋 Add your own domain-specific documents
5. 📋 Adjust chunk size and thresholds for your use case
6. 📋 Deploy to production (replace in-memory email store with database)
7. 📋 Add human review interface for escalated tickets

## References

- [FAISS Documentation](https://github.com/facebookresearch/faiss)
- [LangChain FAISS Integration](https://python.langchain.com/docs/integrations/vectorstores/faiss)
- [OpenAI Embeddings API](https://platform.openai.com/docs/guides/embeddings)
