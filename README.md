# CS6440_Practicum_G095

## Project Overview

This project is an **AI-powered summarizer for clinical reports** using FHIR (Fast Healthcare Interoperability Resources) data.

It consists of:

- **Backend:** FastAPI to fetch patient data and generate summaries (currently using placeholder summarization).
- **Frontend:** Streamlit interface for patients or clinicians to view summaries and visualizations.
- **Data:** FHIR-like data for testing. Real FHIR servers or synthetic data can be integrated later.

---

## Folder Structure

```
fhir-ai-chatbot/
│
├─ backend/
│   ├─ main.py          # FastAPI backend
│   ├─ fhir_client.py   # Fetch FHIR data
│
├─ frontend/
│   ├─ app.py           # Streamlit frontend
│
├─ data/
│   └─ data.json        # FHIR data
```

---

## Setup Instructions

### 1. Clone Repository

```bash
git clone https://github.gatech.edu/rzhang702/CS6440_Practicum_G111.git
cd CS6440_Practicum_G111
```

### 2. Setup Environment and Dependencies

```bash
uv sync
```

This creates a virtual environment and installs all dependencies automatically.

### 3. Add API Key

Copy the example environment file and add your Gemini API key:

```bash
cp .env.example .env
```

Edit `.env` and replace `your_gemini_api_key_here` with your actual API key

### 4. Add Dependencies

To add new packages, edit `pyproject.toml` in the `dependencies` section, then run `uv sync`.

### 5. Run the Agent

```bash
uv run cli_interface.py
```

### 6. Run the API server
```bash
uv run python Backend/main.py
```

then go to http://localhost:8000/docs

### 7. Run the Frontend
```bash
uv run streamlit run Frontend/app.py
```

---

## Local Testing Setup

### 1. Start FHIR Server

Start the local HAPI FHIR server using Docker:

```bash
docker-compose up -d
```

### 2. Run the Agent

```bash
uv run testing_interface.py
```

---

## Github Commands

1. **Pull latest changes**:

```bash
git checkout main
git pull origin main
```

2. **Create a branch if needed**:

```bash
git checkout -b <your name>
```

3. **Make changes and test locally**

4. **Stage and commit**:

```bash
git add .
git commit -m "Add <update description>"
```

5. **Push branch and create PR**:

```bash
git push origin <your name>
```

- Review → merge once approved.