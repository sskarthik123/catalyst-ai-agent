# SkillPilot AI 🚀

## AI-Powered Skill Assessment & Personalized Learning Plan Agent

Built for **Deccan AI Catalyst Hackathon**

---

## Problem Statement

A resume only tells recruiters what a candidate claims to know.

It does **not validate actual proficiency** in those skills.

Recruiters often face problems like:

- Resume keyword stuffing
- No real skill validation
- Poor hiring decisions
- No structured upskilling recommendations for rejected candidates

---

## Our Solution

**SkillPilot AI** bridges this gap by:

1. Extracting skills from candidate resumes
2. Extracting required skills from job descriptions
3. Performing skill gap analysis
4. Conducting real-time AI-generated skill assessments
5. Evaluating candidate responses
6. Showing ideal answers for learning
7. Generating personalized learning roadmaps

---

# Core Features

## 1. Resume Skill Extraction
- Upload resume PDF
- Extracts candidate technical skills

Example:

- C++
- Python
- SQL
- Linux
- Debugging
- APIs

---

## 2. Job Description Skill Extraction
Extracts required skills directly from JD text.

Example:

- C++
- Linux
- Makefiles
- Debugging
- Unix

---

## 3. Pre Skill Gap Analysis
Compares:

Candidate Skills vs Required Skills

Outputs:

- Matched skills
- Missing skills
- Current strengths
- Skill gaps

---

## 4. Dynamic Skill Assessment
Generates:

- Basic to intermediate level questions
- Practical technical questions
- Randomized question generation
- Timer-based assessment flow

---

## 5. Candidate Evaluation Engine
Evaluates responses and classifies users into:

- No Knowledge
- Beginner
- Intermediate
- Advanced

---

## 6. Question Review System
After assessment submission:

- Shows question asked
- Shows candidate answer
- Shows ideal answer

This helps candidates learn immediately.

---

## 7. Personalized Learning Roadmap
For missing skills:

- Priority level
- Estimated learning time
- Free YouTube resources
- Free reading resources

---

# Architecture Flow

```text
Resume Upload
    ↓
Resume Skill Extraction
    ↓
Job Description Skill Extraction
    ↓
Pre Gap Analysis
    ↓
AI Assessment Generation
    ↓
Candidate Answers
    ↓
Answer Evaluation
    ↓
Question Review
    ↓
Learning Roadmap
```

---

# Tech Stack

### Frontend
- Streamlit

### Backend
- Python

### AI/LLM
- Groq API (Llama 3.1)

### Resume Parsing
- PyPDF

### Configuration
- Python Dotenv

### Timer Handling
- Streamlit Auto Refresh

---

# Project Structure

```text
catalyst-ai-agent/
│
├── app.py
├── parser.py
├── pre_gap.py
├── assessment.py
├── evaluator.py
├── planner.py
├── requirements.txt
├── README.md
├── .env.example
└── .gitignore
```

---

# Installation Setup

## Clone repository

```bash
git clone YOUR_GITHUB_REPO_URL
cd catalyst-ai-agent
```

---

## Create Virtual Environment

### Windows (PowerShell)

Create virtual environment:

```bash
python -m venv venv
```

Activate virtual environment:

```powershell
.\venv\Scripts\Activate.ps1
```

---

### Windows (Command Prompt)

```cmd
venv\Scripts\activate
```

---

### Linux / Mac

Create virtual environment:

```bash
python3 -m venv venv
```

Activate virtual environment:

```bash
source venv/bin/activate
```

---

## Install dependencies

```bash
pip install -r requirements.txt
```

---

# API Setup

This project uses Groq API.

Create a `.env` file in root folder:

```env
GROQ_API_KEY=your_actual_groq_api_key
```

You can generate your free API key from:

https://console.groq.com/

---

# Run Project

```bash
streamlit run app.py
```

---

# Example Use Case

### Candidate Resume Skills:
- C++
- Python
- SQL
- Debugging

### Job Description Skills:
- C++
- Linux
- Makefiles
- Debugging

### System Output:
✅ Matched skills  
✅ Missing skills  
✅ Assessment questions  
✅ Skill evaluation  
✅ Learning roadmap  

---
# Please follow the above mentioned steps to upload the resume and validate against JD and skill assessment.

---
# Demo Video
https://drive.google.com/file/d/1_kcvxfD0nzvx3zyqNviVNJwSKsBUv6Ms/view?usp=drive_link

---

# Project URL
https://github.com/sskarthik123/catalyst-ai-agent

---

# Author

**Sornapudi Sai Karthik**

Built during Deccan AI Catalyst Hackathon.
