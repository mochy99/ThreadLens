ana
# ThreadLens

### AI-Powered Discussion Analytics Platform

ThreadLens is a full-stack AI-powered application that transforms unstructured educational discussions into structured, actionable insights.

Inspired by support analytics platforms, ThreadLens analyzes Piazza-style discussions to identify recurring questions, summarize conversations, classify topics, and track unresolved issues.

> **Status:** 🚧 In Development

## 🎯 Problem

University courses generate hundreds of discussion threads on platforms such as Piazza. These discussions contain valuable information about student difficulties, common misconceptions, and recurring technical problems.

However, manually reviewing these conversations is time-consuming and inefficient.

Common challenges include:

- Important questions getting buried in lengthy discussions.
- Students repeatedly asking similar questions.
- Instructors struggling to identify frequently misunderstood concepts.
- Limited visibility into unresolved questions.
- Difficulty tracking discussion trends over time.

## 💡 Solution

ThreadLens uses AI and natural language processing (NLP) to automatically analyze course discussions and present meaningful insights through an interactive dashboard.

The platform aims to help students, teaching assistants, and instructors understand discussion activity without manually reviewing every thread.

## ✨ Planned Features

### 1. AI-Powered Discussion Analysis

- Automatically summarize lengthy discussion threads.
- Classify questions into relevant topic categories.
- Identify resolved and unresolved questions.
- Estimate question urgency based on context.
- Extract key insights from student and instructor responses.

### 2. Interactive Dashboard

- Display total, resolved, and unresolved discussions.
- Visualize discussion activity over time.
- Identify frequently discussed topics.
- Filter discussions by category, status, and urgency.
- Search discussions using keywords.

### 3. Semantic Similarity Detection

- Detect semantically similar questions.
- Group related discussions using text embeddings.
- Identify recurring student misconceptions.
- Reduce duplicate question analysis.

### 4. Automated Reports

- Generate weekly discussion summaries.
- Highlight frequently asked questions.
- Identify unresolved or recurring issues.
- Export structured analytics reports.

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| Frontend | React, TypeScript, Tailwind CSS |
| Backend | Python, FastAPI |
| Database | PostgreSQL |
| AI/NLP | LLM API, Sentence Transformers |
| Data Processing | Pandas |
| Visualization | Recharts |
| Testing | Pytest, React Testing Library |
| Version Control | Git, GitHub |

> The technologies listed above represent the planned stack and may change during development.

## 🏗️ System Architecture

```text
            Piazza-Style Discussion Data
                    (JSON / CSV)
                          |
                          v
                 FastAPI Backend
                          |
                          v
                  Data Processing
                          |
                          v
                  AI/NLP Pipeline
                    /     |     \
                   v      v      v
              Summarize Classify Detect
                                 Issues
                    \     |     /
                          v
                 PostgreSQL Database
                          |
                          v
                       REST API
                          |
                          v
                   React Frontend
                          |
                          v
                 Analytics Dashboard
```

## 📁 Project Structure

The planned repository structure is:

```text
threadlens/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   │   ├── posts.py
│   │   │   └── analytics.py
│   │   ├── models/
│   │   ├── services/
│   │   │   ├── analyzer.py
│   │   │   ├── classifier.py
│   │   │   └── summarizer.py
│   │   └── database.py
│   ├── tests/
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── App.tsx
│   └── package.json
│
├── data/
│   ├── piazza_posts.json
│   └── piazza_posts.csv
│
├── README.md
├── .gitignore
└── .env.example
```

## 📊 Dataset

ThreadLens initially uses synthetic Piazza-style discussion data for development and testing.

Each discussion includes:

| Field | Description |
|-------|-------------|
| `id` | Unique discussion identifier |
| `course` | Course identifier |
| `title` | Discussion title |
| `content` | Original question |
| `tags` | Topic labels |
| `created_at` | Creation timestamp |
| `answers` | Student or instructor responses |
| `followups` | Additional discussion messages |
| `is_resolved` | Resolution indicator |
| `status` | Discussion status |
| `ai_analysis` | Example AI analysis output |

The initial dataset contains 50 synthetic discussions representing common computer science course questions.

No real student information is required.

## 🚀 Getting Started

> Setup instructions describe the planned development environment. They will be verified as implementation progresses.

### Prerequisites

- Python 3.11+
- Node.js 20+
- PostgreSQL
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/threadlens.git
cd threadlens
```

### 2. Backend Setup

```bash
cd backend

python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows
# venv\Scripts\activate

pip install -r requirements.txt
```

Start the backend server:

```bash
uvicorn app.main:app --reload
```

Backend URL:

http://localhost:8000

Interactive API documentation:

http://localhost:8000/docs

### 3. Frontend Setup

Open a new terminal:

```bash
cd frontend

npm install
npm run dev
```

The development server will display the local frontend URL.

## 🔌 Planned API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/posts` | Retrieve discussions |
| GET | `/api/posts/{id}` | Retrieve a discussion |
| GET | `/api/analytics` | Retrieve discussion statistics |
| GET | `/api/topics` | Retrieve topic distributions |
| POST | `/api/analyze` | Analyze discussion content |
| GET | `/api/reports` | Retrieve generated reports |

These endpoints are planned and are not yet guaranteed to be implemented.

## 🧠 AI Analysis Pipeline

The planned AI pipeline consists of five stages.

**1. Data Ingestion**

Load structured discussion data from JSON or CSV files.

**2. Text Preprocessing**

Clean discussion content, normalize text, and prepare it for analysis.

**3. Topic Classification**

Categorize discussions into topics such as:

- Assignments
- Exams
- Lectures
- Debugging
- Course administration

**4. Summarization and Issue Detection**

Generate concise summaries, identify recurring questions, and classify discussion status.

**5. Analytics Generation**

Aggregate the results into metrics and visualizations for the dashboard.

## 🗺️ Development Roadmap

- [ ] Create and validate synthetic Piazza dataset
- [ ] Implement FastAPI REST endpoints
- [ ] Build React dashboard
- [ ] Add discussion filtering and search
- [ ] Implement AI-powered summarization
- [ ] Implement topic classification
- [ ] Add semantic similarity detection
- [ ] Integrate PostgreSQL
- [ ] Generate automated analytics reports
- [ ] Add unit and integration tests
- [ ] Deploy the application

## 🔮 Future Improvements

- Authorized Piazza API integration
- Multi-course analytics
- Semantic search with vector embeddings
- Automatic duplicate question detection
- Instructor feedback for AI-generated classifications
- Real-time discussion monitoring where supported
- Support for additional educational discussion platforms

## 🔒 Privacy and Responsible AI

ThreadLens is developed with student privacy in mind.

- Synthetic data is used during initial development.
- Real discussion data requires appropriate authorization.
- Personally identifiable information should be protected.
- AI-generated classifications and summaries may contain errors.
- Sensitive student discussions should not be exposed publicly.

## 🎓 Project Motivation

ThreadLens is a portfolio project combining full-stack software engineering, natural language processing, and data analytics.

The project focuses on practical engineering challenges, including:

- REST API development
- Data modeling and database design
- AI integration
- Semantic text analysis
- Frontend development
- Automated testing
- Scalable application architecture

## 📄 License

A license has not yet been selected.

---

**ThreadLens — Turning Discussions into Actionable Insights.**
