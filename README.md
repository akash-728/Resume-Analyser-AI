# Resume Analyser

A simple Streamlit application that extracts text from a resume PDF and uses the free-tier Groq API model `qwen/qwen3.6-27b` to review it for a Full Stack Developer role.

## Features

- Upload one text-based PDF resume.
- Analyse clarity, skills, experience descriptions, and Full Stack Developer fit.
- Receive an overall rating and checklist.
- Generate a refined, ATS-friendly resume draft without inventing facts.

## Architecture

```text
Streamlit UI (main.py)
        |
        v
PDF upload -> pypdf text extraction
        |
        v
Prompt with six review sections -> Groq Chat Completions API
        |
        v
Markdown analysis rendered in the browser
```

All application code intentionally lives in `main.py`.

## Workflow

1. The user uploads a PDF and clicks **Analyse Resume**.
2. `pypdf` extracts text from each page.
3. The app sends the extracted text and a structured review prompt to Groq.
4. The model responds with these sections:
   - Content Clarity & Impact
   - Skills Presentation
   - Experience Descriptions
   - Specific Recommendations for Full Stack Developer
   - Overall Rating & Checklist
   - Refined Resume
5. Streamlit renders the Markdown response.

## Setup

### 1. Create and activate the virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Windows Command Prompt:

```bat
python -m venv .venv
.venv\Scripts\activate
```

### 2. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configure the Groq API key

Get a Groq API key from [console.groq.com](https://console.groq.com/), then add these values to `.env`:

```dotenv
GROQ_API_KEY=your-api-key
GROQ_MODEL=qwen/qwen3.6-27b
```

You may also enter the key in the app sidebar. Change `GROQ_MODEL` to any model available in your Groq account. Do not commit API keys to source control.

### 4. Start the app

```powershell
streamlit run main.py
```

Open the local URL printed by Streamlit, upload a resume PDF, and click **Analyse Resume**.

## Notes

- Scanned/image-only PDFs may not contain extractable text. Run OCR first if needed.
- The model name is kept as requested: `qwen/qwen3.6-27b`. Confirm that this model is available in your Groq account before use.
- Resume content is sent to Groq for analysis. Avoid uploading sensitive documents unless you are comfortable with that processing.
