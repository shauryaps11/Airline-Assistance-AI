# SkyAssist — Multi-Modal AI Airline Support Agent

A production-grade airline customer support agent built with GPT-4o function calling, intent-based tool routing, persistent conversation memory (ChromaDB), and automated escalation logic. Served via a React frontend with a session analytics dashboard.

## Architecture

```
React (Vite + TypeScript)        FastAPI Backend
  ChatWindow + IntentBadge  ──►  POST /chat
  EscalationBanner               ├── Intent classifier (GPT-4o JSON mode)
  ImagePanel (DALL·E 3)          ├── ChromaDB memory (local, no API key)
  AnalyticsDashboard  ◄──  GET /analytics
                                 ├── Tool dispatch by intent
                                 │     price_inquiry → get_ticket_price()
                                 │     destination_image → DALL·E 3
                                 ├── Escalation detection + GPT-4o summary
                                 └── SQLite session logging
```

## Requirements

- Python 3.9+
- Node.js 18+
- An `OPENAI_API_KEY` in a `.env` file at the project root

**No other API keys needed.** ChromaDB and SQLite run fully locally.

## Setup

```bash
# 1. Clone and enter the project
cd Airline-Assistance-AI-main

# 2. Copy the env template and add your key
cp .env.example .env
# Edit .env → set OPENAI_API_KEY=sk-...

# 3. Install Python deps
pip3 install -r requirements.txt

# 4. Install frontend deps
cd frontend && npm install && cd ..
```

## Running

**Terminal 1 — backend:**
```bash
python3 -m uvicorn backend.main:app --reload
```

**Terminal 2 — frontend:**
```bash
cd frontend && npm run dev
```

Open `http://localhost:5173`

## Features

| Feature | Detail |
|---|---|
| Intent routing | Classifies message before choosing tools — no blind GPT dispatch |
| Persistent memory | ChromaDB retrieves semantically relevant past turns per session |
| Escalation logic | Auto-detects complaints, low-confidence, keywords → human handoff |
| Multi-modal | DALL·E 3 destination images + TTS-1 voice responses |
| Session analytics | Resolution rate, avg tool calls, intent distribution, escalation breakdown |
| Cross-platform audio | MP3 streamed as base64, played in browser (no macOS-only afplay) |

## Supported Destinations

London · Paris · Tokyo · Berlin · New York · Dubai · Sydney · Rome · Barcelona · Singapore
