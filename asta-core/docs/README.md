# Project Atlas – ASTA Core

ASTA (AI Semantic Task Assistant) is the intelligent automation engine at the heart of **Project Atlas**.  
It combines a **FastAPI backend**, **PostgreSQL database**, **NLP-powered FAQ system**, and **n8n automation server** into a production-ready, containerized system.

This guide will help you set up and run ASTA in under **5 minutes**.

---

## 🚀 Quick Start

### 1. Prerequisites
Before you begin, make sure you have the following installed:

- [Docker](https://docs.docker.com/get-docker/) (latest version)
- [Docker Compose](https://docs.docker.com/compose/install/)
- Git

---

### 2. Clone the Repository
```bash
git clone <your-repo-url>
cd project-atlas/asta-core


3. Environment Setup

   Copy the example environment file:

	cp .env.example .env


   Open .env in your editor and update values:

	JWT_SECRET=<your-secret-key>
	DATABASE_URL=postgresql+asyncpg://user:password@db:5432/asta
	EMAIL_SMTP settings (for Gmail integration with n8n)
	Any other sensitive values


4. Build and Start Services

   Run the following to build and launch the stack:

	docker-compose up -d --build


   This will start:

	FastAPI backend → http://localhost:8000
	PostgreSQL database → exposed internally to backend
	n8n automation server → http://localhost:5678


5. Verify the Installation

   Check API docs:

	Swagger UI
	ReDoc

   Create your first user:

	curl -X POST http://localhost:8000/users/ \
	-H "Content-Type: application/json" \
	-d '{"email": "admin@example.com", "password": "securepassword"}'


   Log in and receive JWT:

	curl -X POST http://localhost:8000/login/ \
	-H "Content-Type: application/json" \
	-d '{"email": "admin@example.com", "password": "securepassword"}'


6. Core Features

Task Management:

	POST /tasks/ → create tasks
	GET /tasks/ → list/filter tasks
	PUT /tasks/{id} → update
	DELETE /tasks/{id} → remove

Intelligent FAQ:
	POST /faq/ → add FAQs (admin only)
	POST /faq/ask → ask a question (semantic similarity powered by spaCy)

Automation:

	Mark a task "is_important": true → triggers n8n → sends confirmation email

7. Stopping the Stack
	docker-compose down

   To remove containers, networks, and volumes:
	docker-compose down -v
