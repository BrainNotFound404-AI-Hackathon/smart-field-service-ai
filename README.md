# smart-field-service-ai
## Project Overview
Our project is an AI-powered field service assistant designed to support elevator technicians across the full maintenance cycle. It integrates ticket data, service records, manuals, and telemetry signals to provide real-time troubleshooting recommendations, detects anomalous sensor data, offers voice-guided repair support, and generates structured incident reports. Key features include a multi-agent architecture and knowledge-grounded LLM responses. It enables end-to-end workflow automation — from ticket pick-up to final report generation to significantly improving efficiency, consistency, and technician experience on-site.
## Architecture Overview
smart-field-service-ai/
├── data/                    # Raw data: tickets, logs, manuals, database
├── knowledge_base/         # Retrieval logic using LangChain vector store
├── output/                 # AI-generated suggestions and markdown reports
├── server/                 # Backend logic (FastAPI)
│   ├── api/                # REST API routes
│   ├── database/           # SQLite schema + operations
│   ├── model/              # Pydantic schemas (Ticket, Response)
│   ├── service/            # Business logic (ticket service)
│   ├── run_service.py      # Entry point for FastAPI
│   ├── agent.py            # LangChain agent logic
│   └── ...
├── frontend/               # (Optional) Frontend app (e.g., React/Vue)
├── requirements.txt        # Python dependencies
└── README.md               # This file
## Architecture Overview of this project
- **Backend**(include in this repository): Handles ticket management, LLM-based troubleshooting suggestions, and structured report generation.
- **Frontend**(include in fix-wise repoistory): Displays ticket list, status, report cards, and allows chat-based interaction (if available).
- **Data Layer**(include in this repository): Local SQLite database for tickets, alerts, and repair history.
## Tech Stack
Backend: FastAPI, Pydantic, SQLite
LLM: Google Gemini 2.0 Flash (via langchain-google-genai)
AI Tooling: LangChain
Database: SQLite 
## Sample Data
fix-wise.db: The database integrates elevator maintenance ticket records with a vectorized knowledge base of manual content to support AI-powered fault diagnosis and troubleshooting.
manual_kb--Stores raw manual fragments or documents.
manual_kb_vec--Main table for embedding vectors representing each manual fragment.
manual_kb_vec_chunks--Contains text chunks that were split from full manuals for vectorization.
manual_kb_vec_info--Stores metadata about the embedding model (e.g., vector dimension, model type).
manual_kb_vec_rowids--Maps vector entries to their corresponding original rows.
manual_kb_vec_vector_chunks00--Stores actual embedding vectors, often in binary or float format.
sqlite_sequence--Tracks the auto-increment values for tables
ticket--Stores elevator maintenance ticket, including details such as elevator ID, fault description, status, priority, timestamps, and AI-generated suggestions.
## Development Tips
Add your Gemini API key in .env:
GOOGLE_API_KEY=sk-xxxxxxx
Modify LLM model in ticket_service.py if needed
Extend new endpoints under server/api/
## Reference
LangChain Docs
Gemini API Reference
