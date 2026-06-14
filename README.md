# ⚡ PromptCraft Studio Pro

> Advanced Prompt Engineering Workspace powered by Google Gemini — 7 AI Modes, Multi-Model, fully interactive dark UI.

---

## 🚀 What I Built

PromptCraft Studio Pro is a Streamlit-based prompt engineering playground that lets you send any input to Google Gemini and instantly reshape how the AI responds — just by switching modes. Each mode injects a different system prompt persona, completely changing the tone, format, and depth of the output.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🎨 **7 Prompt Modes** | ELI5, First Principles, Quiz Master, Code Mentor, Study Blueprint, Interview Coach, Devil's Advocate |
| 🤖 **Multi-Model Support** | Switch between `gemini-1.5-flash` and `gemini-1.5-pro` live |
| 🌡️ **Temperature Slider** | Control creativity from 0.0 (precise) to 1.0 (creative) |
| 📊 **Session Stats** | Live query count, message count, session start time |
| ⏱️ **Query Timeline** | Scrollable log of every query with timestamps and model info |
| 🛠️ **Prompt Debug Layer** | View raw system prompt injection and full JSON payload |
| 📥 **Dual Export** | Download any response as `.md` or `.txt` with metadata |
| 💬 **Chat History** | Persistent multi-turn conversation within session |
| 📈 **Word & Char Count** | Live stats on every AI response |
| 🗑️ **Clear & Reset** | One-click session wipe |

---

## 🎯 Prompt Modes Explained

### 👶 Explain Like I'm 5
Breaks down any complex topic using simple analogies, short sentences, and zero jargon. Ends with a surprising fun fact.

### 📊 System Thinker (First Principles)
Deconstructs topics into foundational truths and rebuilds understanding step-by-step using Socratic reasoning chains.

### 🧠 Interactive Quiz Master
Transforms any topic into a 3-question multiple-choice quiz with progressive difficulty and detailed answer explanations.

### 💻 Code Mentor & Debugger
Analyzes code like a FAANG Staff Engineer — diagnosis, refactored output, inline comments, complexity analysis, and best practices.

### 📅 Actionable Study Blueprint
Builds a 4-week learning roadmap with daily goals, key concepts, curated resources, mini-projects, and self-checks.

### 🎯 Socratic Interview Coach
Generates 5 role-specific interview questions with what interviewers are really testing, model STAR answers, and common mistakes.

### 🔥 Devil's Advocate
Challenges every assumption in your input with the strongest possible counter-arguments. Forces rigorous thinking.

---

## 🛠️ Setup & Installation

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/ai-prompt-architect.git
cd ai-prompt-architect
```

### 2. Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add your API key
Create a `.env` file in the project root:
```
GEMINI_API_KEY=your_actual_gemini_api_key_here
```
Get your free key at: https://aistudio.google.com/app/apikey

### 5. Run the app
```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`

---

## 📁 Project Structure

```
ai-prompt-architect/
├── app.py               # Main application
├── .env                 # API key (never commit this)
├── .gitignore           # Ignores secrets and cache
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

---

## 🔒 Security Notes

- Your `.env` file is listed in `.gitignore` and will **never** be pushed to GitHub
- API keys are loaded via `python-dotenv` at runtime only
- No keys are hardcoded anywhere in the source

---

## 🧰 Tech Stack

- **Frontend / Server:** Streamlit
- **LLM:** Google Gemini 1.5 Flash / Pro via `google-generativeai`
- **Config:** `python-dotenv`
- **Language:** Python 3.10+
- **OS:** Pop!_OS / Ubuntu / any Linux

---

## 📸 Screenshots

> Add your screenshots here after recording your demo video.

---

## 🎥 Demo Video

> Link your ~2 minute demo video here.

---

## 📄 License

MIT License — free to use, modify, and distribute.
