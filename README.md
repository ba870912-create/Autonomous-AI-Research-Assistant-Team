
---

# 🔬 Autonomous AI Research Assistant Team

An autonomous multi-agent research system built with **CrewAI**, **FastAPI**, and **Streamlit**. Give it a research topic and it will search the web, analyze sources, and generate a full academic report with citations.

---

## 🚀 Features

- 🤖 **5 Specialized AI Agents** working together
- 🔍 **Web Search** via Serper API
- 📚 **arXiv Search** for academic papers
- 🌐 **Web Scraping** with Playwright
- 📝 **Full Research Reports** with APA/MLA/Chicago citations
- ⚡ **Async Job Processing** — no waiting for the UI to freeze
- 🖥️ **Streamlit Frontend** + **FastAPI Backend**

---

## 🧠 Agent Architecture

| Agent | Role |
|-------|------|
| 🎯 Research Coordinator | Plans the search strategy and keywords |
| 🔍 Web Search Agent | Searches the web and arXiv, scrapes top URLs |
| 📊 Content Analyzer | Extracts key findings and themes from sources |
| ✍️ Synthesis Agent | Writes the full research report |
| 📖 Citation Manager | Adds citations and formats references |

---

## 🛠️ Tech Stack

- **Agents**: [CrewAI](https://crewai.com) v1.14.4
- **LLM**: Groq (llama-3.3-70b-versatile) — free tier
- **Backend**: FastAPI + Uvicorn
- **Frontend**: Streamlit
- **Search**: Serper API
- **Academic Search**: arXiv
- **Web Scraping**: Playwright + Markdownify

---

## ⚙️ Setup

### 1. Clone the repo
```bash
git clone https://github.com/your-username/Autonomous-AI-Research-Assistant-Team.git
cd Autonomous-AI-Research-Assistant-Team
```

### 2. Create a virtual environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
pip install litellm playwright markdownify
playwright install chromium
```

### 4. Set up environment variables
Create a `.env` file in the root directory:
```env
GROQ_API_KEY=your-groq-api-key
SERPER_API_KEY=your-serper-api-key
```

Get your free API keys:
- 🔑 **Groq**: [console.groq.com](https://console.groq.com) — free, no credit card
- 🔑 **Serper**: [serper.dev](https://serper.dev) — 2500 free searches

---

## ▶️ Running the App

### Start the backend (Terminal 1)
```bash
uvicorn backend.main:app --reload --port 8000
```

### Start the frontend (Terminal 2)
```bash
streamlit run frontend/app.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 📁 Project Structure

```
├── backend/
│   ├── main.py
│   ├── crew.py
│   ├── agents/
│   ├── tools/
│   └── db/
├── frontend/
│   └── app.py
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/research` | Start a research job |
| GET | `/research/{job_id}` | Get job status and result |

---

## ⚠️ Known Limitations

- Groq free tier has a **12,000 token/minute** limit — wait ~30 seconds between requests
- Web scraping may fail on JavaScript-heavy sites
- Results are stored **in-memory** — lost on server restart

---

## 📄 License

MIT License
