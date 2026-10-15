# ThreadLens

**AI-Powered Educational Discussion Analytics Platform**

ThreadLens is a full-stack application that transforms educational discussion posts into structured insights. It helps instructors understand student questions, monitor unresolved discussions, identify recurring topics, and generate AI-powered course summaries.

The project uses a React and TypeScript frontend, a FastAPI backend, and a locally hosted Llama 3.2 model through Ollama.

## Features

- **Discussion Dashboard:** Visualize total discussions, resolution status, and common topics.
- **Issue Analyzer:** Generate AI-powered summaries, topic classifications, urgency levels, and keywords for individual discussions.
- **Course Summarizer:** Aggregate discussion statistics and generate course-level insights and suggested instructor actions.
- **Discussion Explorer:** Browse educational discussions and inspect their analysis.
- **REST API:** Access discussion data, analytics, and AI analysis through FastAPI.
- **Local AI Processing:** Run Llama 3.2 locally using Ollama without requiring a paid LLM API.

**Additional prototype functionality:** Semantic similarity detection for identifying related discussions. This backend feature is experimental and is not yet integrated into the dashboard.

## Tech Stack

| Layer | Technologies |
|---|---|
| Frontend | React, TypeScript, Vite |
| Styling | CSS |
| Charts | Recharts |
| Backend | Python 3.11, FastAPI, Uvicorn |
| LLM | Llama 3.2, Ollama |
| Data Storage | Local JSON dataset |

## Project Architecture

```text
ThreadLens/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── posts.py
│   │   │   ├── analytics.py
│   │   │   ├── analyze.py
│   │   │   ├── similarity.py
│   │   │   └── summarizer.py
│   │   ├── services/
│   │   │   ├── analyzer.py
│   │   │   ├── llm_analyzer.py
│   │   │   ├── similarity.py
│   │   │   └── summarizer.py
│   │   └── main.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── IssueAnalyzer.tsx
│   │   │   └── Summarizer.tsx
│   │   ├── services/
│   │   │   └── api.ts
│   │   └── App.tsx
│   └── package.json
├── data/
│   └── piazza_posts.json
└── README.md
```

## Getting Started

### Prerequisites

Install the following:

- Python 3.11
- Node.js and npm
- Ollama
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/ThreadLens.git
cd ThreadLens
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Set Up the Backend

Create a Python virtual environment:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

Install backend dependencies:

```bash
cd backend
python -m pip install -r requirements.txt
```

If you have not yet finalized `requirements.txt`, ensure it includes the dependencies used by your backend, including FastAPI, Uvicorn, Ollama, Sentence Transformers, and NumPy.

### 3. Set Up Ollama

Install Ollama from https://ollama.com.

Download the model:

```bash
ollama pull llama3.2:3b
```

Start the Ollama server if it is not already running:

```bash
ollama serve
```

Ollama runs at:

```text
http://127.0.0.1:11434
```

### 4. Start the Backend

Open a terminal in the `backend` directory with your Python virtual environment activated:

```bash
python -m uvicorn app.main:app --reload
```

The backend will run at:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

http://127.0.0.1:8000/docs

### 5. Set Up the Frontend

Open a new terminal:

```bash
cd ThreadLens/frontend
npm install
npm run dev
```

If you are already in the project root, use `cd frontend` instead.

Open the local URL displayed by Vite, typically:

http://localhost:5173

## How to Use

### Discussion Dashboard

The dashboard displays discussion statistics, resolution rates, topic distributions, and recent discussions.

Select a discussion to open the Issue Analyzer.

### AI Issue Analyzer

The Issue Analyzer processes a discussion using Llama 3.2 and returns:

- Summary
- Topic
- Urgency
- Keywords
- Explanation
- Resolution status from discussion metadata

If the LLM is unavailable, the backend can fall back to keyword-based analysis.

### Course Summarizer

Navigate to **Summarizer** in the sidebar.

1. Select a course.
2. Click **Generate Summary**.
3. Wait for the local LLM to analyze the selected discussions.
4. Review the course statistics, common topics, student challenges, and recommended instructor actions.

The initial implementation analyzes up to 20 discussions per report, while overall discussion counts are calculated from the full selected course dataset.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/posts` | Retrieve discussions |
| GET | `/api/posts/{post_id}` | Retrieve a discussion |
| GET | `/api/analytics` | Retrieve dashboard statistics |
| GET | `/api/analytics/topics` | Retrieve topic counts |
| GET | `/api/analyze/{post_id}` | Analyze a discussion |
| GET | `/api/similarity/{post_id}` | Find semantically related discussions |
| GET | `/api/summarizer/courses` | List available courses |
| GET | `/api/summarizer/{course}` | Generate a course summary |

Additional analytics endpoints are documented in FastAPI's interactive API documentation.

## Data and Privacy

ThreadLens currently uses a synthetic Piazza-style discussion dataset stored in `data/piazza_posts.json`.

The project does not require access to private Piazza accounts or student discussions.

LLM inference is performed locally through Ollama.

## Current Limitations

- Uses synthetic discussion data rather than a live Piazza integration.
- Does not currently use a persistent database.
- AI outputs may contain inaccuracies and should be reviewed.
- Course report generation may take time on machines with limited resources.
- Semantic similarity results require threshold tuning and evaluation.
- AI analyses are not currently cached persistently.

## Future Improvements

- PostgreSQL persistence
- LLM response caching
- Automated testing and evaluation
- Docker-based setup
- Improved search and filtering
- Production deployment

## Project Purpose

ThreadLens was developed as a full-stack software engineering and applied AI project to explore how large language models can transform unstructured educational discussions into useful, actionable insights.

It demonstrates REST API development, frontend engineering, data visualization, natural language processing, and local LLM integration.

## License

Add a license file if you choose to release the project under an open-source license.