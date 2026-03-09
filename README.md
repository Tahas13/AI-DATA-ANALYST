# 🤖 AI Data Analyst 2.0

An AI-powered natural language data analyst built with **Streamlit**, **LangChain**, and **Ollama**. Ask questions about your database in plain English and get instant SQL-powered results.

---

## ✨ Features

- 💬 Natural language to SQL conversion using a local LLM (via Ollama)
- 📊 Clean, interactive data table results
- 🔍 Shows the generated SQL query for transparency
- ⚡ Auto-retry on SQL errors with error feedback to the LLM
- 🔒 Fully local — your data never leaves your machine

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | [Streamlit](https://streamlit.io) |
| LLM Orchestration | [LangChain](https://langchain.com) |
| Local LLM | [Ollama](https://ollama.com) (`llama3.2:3b`) |
| Database | SQLite + [SQLAlchemy](https://sqlalchemy.org) |
| Package Manager | [uv](https://github.com/astral-sh/uv) |

---

## 🚀 Getting Started

### Prerequisites

- [Python 3.12+](https://python.python.org)
- [Ollama](https://ollama.com) installed and running
- [uv](https://github.com/astral-sh/uv) installed

### 1. Clone the repository

```bash
git clone https://github.com/Tahas13/AI-DATA-ANALYST.git
cd AI-DATA-ANALYST
```

### 2. Install dependencies

```bash
uv sync
```

### 3. Pull the LLM model

```bash
ollama pull llama3.2:3b
```

### 4. Create the database

```bash
uv run python create_database.py
```

### 5. Run the app

```bash
uv run streamlit run frontend.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 💡 Example Questions

- *"What is the most sold product?"*
- *"Show me total revenue by category"*
- *"List the top 5 customers by order count"*
- *"How many orders were placed this year?"*

---

## 📁 Project Structure

```
AI-DATA-ANALYST/
├── frontend.py          # Streamlit UI
├── main.py              # LLM + database logic
├── create_database.py   # Database creation script
├── pyproject.toml       # Project dependencies
└── README.md
```

---

## ⚠️ Note on Deployment

This project uses **Ollama running locally**. To deploy it publicly, you can either:
- Host everything on a cloud VM (e.g. AWS EC2, DigitalOcean)
- Replace Ollama with a cloud LLM API (e.g. [Groq](https://groq.com) — free tier available)

---

## 📄 License

MIT
