# smart-field-service-ai

## Project Overview
**Smart Field Service AI** is an AI-powered assistant that supports elevator technicians throughout the entire maintenance lifecycle. It integrates service tickets, historical logs, technical manuals, and telemetry data to:

- Provide real-time troubleshooting recommendations
- Detect anomalies in sensor signals
- Offer voice-guided repair support
- Automatically generate structured incident reports

The system uses a **multi-agent architecture** and **knowledge-grounded LLM responses** to enable **end-to-end automation** — from ticket creation to report generation — improving on-site efficiency, consistency, and technician experience.

---

## 📦 Project Structure
smart-field-service-ai/
├── data/ # Raw data: tickets, logs, manuals, database

├── knowledge_base/ # LangChain vector store + retrieval logic

├── output/ # AI-generated suggestions and markdown reports

├── server/ # Backend logic (FastAPI)

│ ├── api/ # REST API routes

│ ├── database/ # SQLite schema + operations

│ ├── model/ # Pydantic schemas (Ticket, Response)

│ ├── service/ # Business logic layer

│ ├── run_service.py # FastAPI entry point

│ ├── agent.py # LangChain agent logic

├── frontend/ # (Optional) Frontend app (e.g., React/Vue)

├── requirements.txt # Python dependencies

└── README.md # Project documentation


---

## ⚙️ Architecture Summary

- **Backend** *(this repository)*: Handles ticket management, AI-powered suggestions, and report generation using FastAPI + LangChain.
- **Frontend** *(in [fix-wise](https://github.com/your-org/fix-wise))*: Displays tickets, statuses, reports, and chat interfaces for field technicians.
- **Database** *(local SQLite)*: Stores tickets, AI suggestions, alerts, and manual embeddings.

---

## 🧰 Tech Stack

| Layer        | Technology                  |
|--------------|-----------------------------|
| Backend      | FastAPI, Pydantic           |
| AI Engine    | LangChain + Gemini 2.0 Flash |
| LLM Provider | Google Generative AI        |
| Database     | SQLite                      |

---

## 🧪 Sample Data: `fix-wise.db`

This SQLite database supports AI-driven troubleshooting by integrating tickets and a vectorized manual knowledge base.

- `ticket`: Elevator maintenance records (ID, location, fault, priority, timestamps, AI suggestions).
- `sqlite_sequence`: Auto-increment tracking for tables.

**Manual Knowledge Base Tables**:
- `manual_kb`: Stores raw manual fragments.
- `manual_kb_vec`: Embedding vectors of manual content.
- `manual_kb_vec_chunks`: Split text chunks used for embedding.
- `manual_kb_vec_info`: Metadata about embedding model and vectorization.
- `manual_kb_vec_rowids`: Mapping between original content and vector entries.
- `manual_kb_vec_vector_chunks00`: Actual vector data (in float or binary format).

---

## 🛠️ Development Tips

- Add your Gemini API key to a `.env` file:
  ```env
  GOOGLE_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx
- Modify LLM model in server/service/ticket_service.py if needed.

- Add new API endpoints under server/api/.

## Reference
LangChain Docs

Gemini API Reference
