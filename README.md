# 🧠 Conversational Context Integrity Monitor

> Detect and visualize **conversational drift**: the moment an LLM forgets what the user told it earlier in a chat.

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-ff4b4b)
![LLM](https://img.shields.io/badge/LLM-Llama%203.1%20on%20Groq-orange)
![Storage](https://img.shields.io/badge/storage-SQLite-lightgrey)

## The problem

In a long conversation, LLMs quietly lose track of earlier details. You say *"my budget is ₹50,000"*, and three messages later you get a laptop suggestion that costs ₹90,000. This is **context drift**, and it's hard to notice while it's happening.

## What this project does

This app wraps an LLM chat with a memory layer and a drift monitor:

1. **Extracts facts** from every user message (budget, location, diet, interests, ...) using an LLM.
2. **Stores them** in a local SQLite database.
3. **Re-injects** the stored facts into every prompt so the model is reminded of them.
4. **Checks the response** to see whether it actually respects the important facts.
5. **Scores the drift** for each turn and shows it live as a bar chart and a trend line.

## Features

- 💬 Streamlit chat interface
- 🧾 Automatic fact extraction, returned as structured JSON (`entity` / `value`)
- 💾 Persistent fact memory in SQLite, visible in the sidebar
- 🔁 Memory re-injection into every prompt
- 🚨 Drift alerts per turn: low, medium, and high
- 📊 Drift-per-turn bar chart and trend line
- 🧹 One-click memory reset

## How it works

```
User message
     │
     ▼
 fact_extractor.py ──► memory_store.py (SQLite)
                              │
                              ▼
                       reinjector.py  (builds "Important facts" block)
                              │
                              ▼
                       llm_wrapper.py ──► Llama 3.1 (Groq) ──► response
                                                                  │
                                                                  ▼
                                                        drift_detector.py
                                                      (which facts were missed?)
                                                                  │
                                                                  ▼
                                                         drift_tracker.py
                                                       (score + history)
                                                                  │
                                                                  ▼
                                                  app.py: alerts + charts
```

### Drift score

Drift is based on how many tracked facts the response failed to mention:

```
drift % = missed / (missed + 1) × 100
```

| Missed facts | Drift score | Alert |
|---|---|---|
| 0 | 0% | none |
| 1 | 50% | ⚠️ Medium |
| 2 | 66.7% | ⚠️ Medium |
| 3+ | 75%+ | 🚨 High |

Only these entities are tracked for forgetting: `budget`, `preference`, `requirement`, `usage`.

## Project structure

| File | Purpose |
|---|---|
| `app.py` | Streamlit UI, chat flow, alerts, and charts |
| `fact_extractor.py` | Extracts `{entity, value}` facts from user text via the LLM |
| `memory_store.py` | SQLite read/write helpers for facts |
| `reinjector.py` | Turns stored facts into a prompt block |
| `llm_wrapper.py` | Thin wrapper around the Groq client |
| `drift_detector.py` | Finds important facts missing from a response |
| `drift_tracker.py` | Calculates and stores the drift score per turn |
| `contradiction_checker.py` | Helper to spot a new value that conflicts with a stored one (not yet wired into the app) |

## Getting started

### Prerequisites

- Python **3.10 or newer**
- A free **Groq API key**: create one at [console.groq.com](https://console.groq.com)

### 1. Clone the repo

```bash
git clone https://github.com/<your-username>/conversational-drift-monitor.git
cd conversational-drift-monitor
```

### 2. Create a virtual environment (recommended)

**Windows (PowerShell):**
```powershell
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set your API key

Never commit your key to GitHub. Set it as an environment variable instead.

**Windows (PowerShell):**
```powershell
$env:GROQ_API_KEY="your_key_here"
```

**macOS / Linux:**
```bash
export GROQ_API_KEY="your_key_here"
```

### 5. Create the database (one time)

```bash
python -c "import sqlite3; c=sqlite3.connect('memory.db'); c.execute('CREATE TABLE IF NOT EXISTS facts (turn INTEGER, entity TEXT, value TEXT)'); c.commit()"
```

### 6. Run the app

```bash
streamlit run app.py
```

Streamlit opens the app at `http://localhost:8501`.

## Try it

Send these messages one at a time and watch the sidebar and charts:

```
My budget is 50000
I want a laptop for programming
Suggest the best option for me
What about gaming laptops?
```

If a response ignores your stored budget or requirement, the drift chart will show a bar for that turn.

## Known limitations

- **Drift detection is keyword-based.** It checks whether the stored value appears as text in the response, so a correct answer worded differently can be flagged as drift.
- **Only four entities are tracked** for forgetting (`budget`, `preference`, `requirement`, `usage`).
- **The "fix" step regenerates with the same prompt.** At `temperature=0` this often returns the same answer.
- **Drift history is kept in memory** and resets when the app restarts. Facts persist in SQLite, and are cleared when a new session starts.
- **Contradictions are not detected yet.** `contradiction_checker.py` exists but isn't used.
- **Single user only.** There are no accounts or per-user memory.

## Roadmap

- [ ] Use the contradiction checker to flag changed facts (e.g. budget revised mid-chat)
- [ ] Semantic matching instead of substring matching for drift detection
- [ ] Corrective re-prompt that explicitly names the missed facts
- [ ] Persist drift history to SQLite
- [ ] Support more providers in `llm_wrapper.py`
- [ ] Export drift reports as CSV

## Tech stack

Python · Streamlit · Groq API (`llama-3.1-8b-instant`) · SQLite · pandas · matplotlib

## Contributing

Issues and pull requests are welcome. For larger changes, please open an issue first to discuss what you'd like to change.

## License

Released under the [MIT License](LICENSE).
