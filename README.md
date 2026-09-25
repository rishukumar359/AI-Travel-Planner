# ✈️ AI Travel Planner — Backend

> An AI-powered, stateful travel planning backend built with **FastAPI, LangGraph, Hugging Face LLMs, SQLAlchemy and SQLite**.

The backend converts a user's natural-language travel request into a structured travel plan by orchestrating multiple AI agents, external travel search tools, validation, Human-in-the-Loop clarification, budget calculation and itinerary generation.

---

## 🚀 Features

### 🤖 AI & Agentic Workflow

* Natural-language travel request processing
* LLM-powered trip information extraction
* Multi-agent workflow using LangGraph
* Stateful workflow execution
* Conditional routing
* Human-in-the-Loop clarification
* Persistent LangGraph checkpointing
* Parallel flight, train and bus searches
* Transport selection
* Hotel search
* Budget calculation
* AI-generated itinerary

### 🔐 Authentication & Security

* User registration
* JWT-based authentication
* Password hashing using bcrypt
* Protected trip APIs
* User-specific trip history
* User-scoped LangGraph thread IDs

### 🗄️ Database & Persistence

* SQLAlchemy ORM
* SQLite database
* User persistence
* Trip persistence
* Trip history API
* Persistent LangGraph checkpoint database

### ⚙️ Backend Engineering

* FastAPI REST APIs
* Pydantic request/response validation
* Centralized exception handling
* Structured application logging
* Request ID tracking
* Database transaction rollback handling
* API timeout handling
* Modular backend architecture

---

# 🏗️ Architecture

```text
                         ┌──────────────────┐
                         │   Client / UI    │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │     FastAPI      │
                         │    REST APIs     │
                         └────────┬─────────┘
                                  │
                     ┌────────────┼────────────┐
                     │            │            │
                     ▼            ▼            ▼
                  Auth API     Trip API     History API
                     │            │
                     │            ▼
                     │       ┌───────────┐
                     │       │ LangGraph │
                     │       └─────┬─────┘
                     │             │
                     │      ┌──────┴──────┐
                     │      │             │
                     │      ▼             ▼
                     │   Planner       Validator
                     │                     │
                     │              ┌──────┴──────┐
                     │              │             │
                     │              ▼             ▼
                     │            HITL         Continue
                     │                            │
                     │                            ▼
                     │                   Parallel Search
                     │                  ┌─────┬─────┬─────┐
                     │                  ▼     ▼     ▼
                     │               Flight Train  Bus
                     │                  └─────┬─────┘
                     │                        ▼
                     │                 Transport Agent
                     │                        │
                     │                        ▼
                     │                   Hotel Search
                     │                        │
                     │                        ▼
                     │                 Budget Calculator
                     │                        │
                     │                        ▼
                     │                 Itinerary Agent
                     │                        │
                     │                        ▼
                     │                  Final Response
                     │
                     ▼
                  SQLite
```

---

# 🔄 LangGraph Workflow

The travel planning workflow is state-driven.

```text
User Query
    │
    ▼
Planner Agent
    │
    ▼
Validator
    │
    ├──────── Missing information ────────► Human-in-the-Loop
    │                                             │
    │                                             ▼
    │                                      User Clarification
    │                                             │
    │                                             ▼
    │                                      Resume Workflow
    │
    └──────── Complete ─────────► Parallel Transport Search
                                      │
                         ┌────────────┼────────────┐
                         ▼            ▼            ▼
                      Flight        Train         Bus
                         └────────────┼────────────┘
                                      ▼
                              Transport Agent
                                      │
                                      ▼
                                Hotel Search
                                      │
                                      ▼
                              Budget Calculator
                                      │
                                      ▼
                              Itinerary Agent
                                      │
                                      ▼
                                Final Result
```

---

# 🧠 Human-in-the-Loop

The application does not blindly allow the LLM to guess missing travel information.

For example:

```text
User:
"Plan a trip to Goa."

        ↓

Planner

        ↓

Validator

        ↓

Missing:
- Origin
- Duration
- Budget

        ↓

Human-in-the-Loop

        ↓

User provides clarification

        ↓

Same workflow thread resumes

        ↓

Trip planning continues
```

LangGraph checkpointing is used to maintain workflow state across the interruption and resume operation.

---

# ⚡ Parallel Processing

Flight, train and bus searches are independent operations.

Instead of:

```text
Flight
  ↓
Train
  ↓
Bus
```

the workflow performs:

```text
              Search Start
              /     |     \
             ↓      ↓      ↓
         Flight   Train   Bus
             \      |      /
              \     |     /
               ▼    ▼    ▼
              Search Complete
```

This allows independent searches to execute concurrently and reduces unnecessary workflow latency.

---

# 🔐 Authentication Flow

```text
Register
   ↓
Password
   ↓
bcrypt Hash
   ↓
SQLite

Login
   ↓
Verify Password
   ↓
Generate JWT
   ↓
Protected APIs
```

Protected endpoints derive the current user from the JWT instead of accepting a client-supplied user ID.

---

# 🗄️ Database

The project currently uses SQLite for local development.

### Main database entities

```text
User
 ├── id
 ├── user_id
 ├── password_hash
 └── created_at

Trip
 ├── id
 ├── user_id
 ├── thread_id
 ├── destination
 ├── duration_days
 ├── transport
 ├── total_budget
 ├── itinerary
 └── created_at
```

A separate SQLite database is used for persistent LangGraph checkpoints.

```text
travel_planner.db
    └── Application data

langgraph_checkpoints.db
    └── LangGraph workflow state
```

---

# 🛠️ Tech Stack

| Category         | Technology          |
| ---------------- | ------------------- |
| Language         | Python              |
| API Framework    | FastAPI             |
| AI Orchestration | LangGraph           |
| LLM              | Hugging Face / Qwen |
| LLM Framework    | LangChain           |
| Authentication   | JWT                 |
| Password Hashing | bcrypt              |
| ORM              | SQLAlchemy          |
| Database         | SQLite              |
| Validation       | Pydantic            |
| Frontend         | Streamlit           |
| External APIs    | Travel search APIs  |
| Version Control  | Git                 |

---

# 📁 Project Structure

```text
backend/
│
├── app/
│   ├── agents/
│   │   ├── planner.py
│   │   ├── validator.py
│   │   ├── clarification.py
│   │   ├── transport.py
│   │   ├── budget.py
│   │   └── itinerary.py
│   │
│   ├── graph/
│   │   ├── graph.py
│   │   ├── state.py
│   │   └── checkpointer.py
│   │
│   ├── tools/
│   │   ├── flight.py
│   │   ├── train.py
│   │   ├── bus.py
│   │   └── hotel.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   ├── auth.py
│   │   ├── exceptions.py
│   │   └── logging_config.py
│   │
│   ├── database/
│   │   ├── connection.py
│   │   └── models.py
│   │
│   └── main.py
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

> Adjust the file names above to match the final repository structure if any modules have different names.

---

# 🔌 API Endpoints

## Authentication

### Register

```http
POST /auth/register
```

Request:

```json
{
  "user_id": "rishu",
  "password": "password123"
}
```

---

### Login

```http
POST /auth/login
```

Request:

```json
{
  "user_id": "rishu",
  "password": "password123"
}
```

Response:

```json
{
  "access_token": "<JWT_TOKEN>",
  "token_type": "bearer"
}
```

---

## Trip Planning

### Plan Trip

```http
POST /trips/plan
```

Requires:

```http
Authorization: Bearer <JWT_TOKEN>
```

Request:

```json
{
  "query": "Plan a 4 day trip from Hyderabad to Goa within 30000",
  "thread_id": "unique-thread-id"
}
```

---

### Clarify Trip

```http
POST /trips/clarify
```

Used when the LangGraph workflow requires additional information from the user.

Request:

```json
{
  "answer": "My budget is 30000 and I prefer train",
  "thread_id": "unique-thread-id"
}
```

The same thread ID is used to resume the interrupted workflow.

---

## Trip History

### Get My Trips

```http
GET /trips
```

Requires:

```http
Authorization: Bearer <JWT_TOKEN>
```

Returns trips belonging to the authenticated user.

---

# ⚙️ Local Setup

## 1. Clone the repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd AI-Travel-Planner-Backend
```

## 2. Create virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Configure environment variables

Create `.env`:

```env
HF_MODEL=Qwen/Qwen2.5-7B-Instruct
HF_TOKEN=your_huggingface_token
JWT_SECRET=your_secret_key
DATABASE_URL=sqlite:///./travel_planner.db
```

Never commit the actual `.env` file.

## 5. Start the backend

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

# 🔒 Security Notes

* Never commit `.env`
* Never expose Hugging Face tokens
* Never expose JWT secrets
* Passwords are stored as bcrypt hashes
* Protected APIs use JWT authentication
* User-specific trip data is filtered using the authenticated user identity

---

# 🧪 API Testing

FastAPI Swagger UI can be used to test the APIs:

```text
/docs
```

Recommended testing flow:

```text
1. Register
      ↓
2. Login
      ↓
3. Copy JWT token
      ↓
4. Authorize in Swagger
      ↓
5. Plan a trip
      ↓
6. Handle clarification if required
      ↓
7. Retrieve trip history
```

---

# 📈 Future Production Improvements

The current application is designed as a strong local/backend prototype. Potential production enhancements include:

```text
Current
   │
   ├── SQLite
   ├── Local process
   └── Local checkpoint storage
          │
          ▼
Future
   │
   ├── PostgreSQL
   ├── Redis
   ├── Celery
   ├── Docker
   ├── Nginx / Load Balancer
   ├── CI/CD
   ├── Cloud deployment
   └── Observability / Monitoring
```

These are planned improvements and are not required for the current local implementation.

---

# 🎯 Key Engineering Concepts Demonstrated

This project demonstrates practical experience with:

* REST API development
* Authentication and authorization
* JWT
* Password hashing
* Database persistence
* ORM usage
* Stateful AI workflows
* Multi-agent orchestration
* Human-in-the-Loop
* Conditional workflow routing
* Parallel task execution
* External API integration
* Request validation
* Error handling
* Logging
* Persistent workflow state
* Modular backend architecture

---

# 👨‍💻 Author

**Rishu Kumar**

Backend / GenAI Developer

Focus areas:

```text
Python
FastAPI
GenAI
LLMs
RAG
Agentic AI
LangGraph
AWS
Backend Engineering
```

---

## ⭐ Project Highlights

> **Stateful Multi-Agent Travel Planning Backend**

Built to demonstrate how LLMs can be integrated with traditional backend engineering, external APIs, persistent state, authentication and deterministic business logic to create a practical AI application.
