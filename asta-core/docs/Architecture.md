
---

### 📄 `ARCHITECTURE.md`
```markdown
# ASTA System Architecture

ASTA (AI Semantic Task Assistant) is a **hybrid local-cloud system** orchestrated with Docker.  
It combines an **intelligent backend (FastAPI + PostgreSQL)**, a **workflow automation server (n8n)**, and **AI-powered FAQ system**.

---

## 🧩 Core Components

### 1. ASTA Core (FastAPI + PostgreSQL)
- **Purpose:** Main backend API, user management, data persistence
- **Technologies:** Python, FastAPI, SQLAlchemy 2.0, Alembic, Pydantic, JWT
- **Responsibilities:**
  - User authentication
  - Task management (CRUD, filtering, sorting)
  - FAQ management + semantic search (spaCy similarity)

---

### 2. NLP Engine
- **Library:** spaCy (`en_core_web_md` model)
- **Purpose:** Extracts semantic meaning and finds the closest FAQ entry
- **Method:** Cosine similarity over word vectors
- **Configurable threshold:** 0.6 (tunable)

---

### 3. n8n (Automation Server)
- **Purpose:** Event-driven automation orchestrator
- **Tech Stack:** Node.js, Docker
- **Key Features:**
  - Listens to webhooks from ASTA Core
  - Sends confirmation emails for important tasks
  - Supports 200+ integrations (Slack, Google Sheets, CRMs, etc.)

---

### 4. PostgreSQL Database
- **Purpose:** Persistent data storage
- **Entities:**
  - `users` → authentication and roles
  - `tasks` → task data, flags, metadata
  - `faqs` → questions, answers, category
- **Migrations:** Managed with Alembic

---

## 🔄 Data Flow Examples

### Task Creation (normal task)

### Task Creation (Important → triggers email)
[User]
   ↓
POST /tasks/ (is_important: true)
   ↓
[ASTA Core → DB]
   ↓
Trigger Webhook → [n8n Workflow]
   ↓
[Gmail API → Confirmation Email]

### FAQ Answering
[User Question]
   ↓
POST /faq/ask
   ↓
[ASTA Core + spaCy Similarity Search]
   ↓
Match best FAQ entry (if score ≥ 0.6)
   ↓
Return JSON { "answer": "…" }

### 📊 ASCII Diagram
                ┌──────────────────┐
                │     Frontend     │
                │ (Future Clients  │
                └───────┬──────────┘
                        │
                        ▼
                ┌──────────────────┐
                │   ASTA Core API  │
                │  (FastAPI App)   │
                └───────┬──────────┘
                        │
         ┌──────────────┼──────────────┐
         ▼                              ▼
┌─────────────────┐            ┌─────────────────┐
│  PostgreSQL DB  │            │   NLP Engine    │
│  (SQLAlchemy)   │            │   (spaCy)       │
└─────────────────┘            └─────────────────┘
         │
         ▼
┌───────────────────────────┐
│         n8n Server        │
│ (Webhook + Gmail workflow)│
└───────────────────────────┘
