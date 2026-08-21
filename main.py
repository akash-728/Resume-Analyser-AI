import os
from io import BytesIO

import streamlit as st
from groq import Groq
from pypdf import PdfReader
from dotenv import load_dotenv

load_dotenv()
MODEL_NAME = os.getenv("GROQ_MODEL", "qwen/qwen3.6-27b")

st.set_page_config(
    page_title="Resume Analyser",
    page_icon="📄",
    layout="centered",
)

st.title("Resume Analyser")
st.write("Upload a resume PDF to get focused feedback for a Full Stack Developer role.")

with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input(
        "Groq API key",
        value=os.getenv("GROQ_API_KEY", ""),
        type="password",
        help="You can also set the GROQ_API_KEY environment variable in .env.",
    )
    st.caption(f"Model: {MODEL_NAME}")

uploaded_file = st.file_uploader("Upload resume PDF", type=["pdf"])


def extract_resume_text(pdf_file) -> str:
    """Extract text from every page in the uploaded PDF."""
    reader = PdfReader(BytesIO(pdf_file.getvalue()))
    pages = [page.extract_text() or "" for page in reader.pages]
    return "\n\n".join(pages).strip()


def analyse_resume(resume_text: str, client: Groq) -> str:
    prompt = f"""You are an expert resume reviewer and hiring manager for Full Stack Developer roles.
Analyse the resume below. Give practical, specific feedback and preserve factual accuracy.
Organise your response with exactly these six Markdown headings:

1. Content Clarity & Impact
2. Skills Presentation
3. Experience Descriptions
4. Specific Recommendations for Full Stack Developer
5. Overall Rating & Checklist
6. Refined Resume

For sections 1-4, cite examples from the resume when useful and provide improved wording where possible.
For section 5, give a score out of 10 and a concise checklist of strengths and gaps.
For section 6, provide a polished, ATS-friendly resume draft based only on information present in the source.
Do not invent employers, dates, metrics, technologies, or achievements. Mark missing information as [add detail].

Resume text:
---
{resume_text}
---
"""
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": "You provide clear, honest, constructive resume analysis.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
    )
    return response.choices[0].message.content


if st.button("Analyse Resume", type="primary", use_container_width=True):
    if not uploaded_file:
        st.warning("Please upload a PDF resume first.")
    elif not api_key:
        st.error("Add a Groq API key in the sidebar or set GROQ_API_KEY before analysing.")
    else:
        try:
            with st.spinner("Extracting resume and generating analysis..."):
                resume_text = extract_resume_text(uploaded_file)
                if not resume_text:
                    st.error("No selectable text was found in this PDF. Try a text-based PDF.")
                    st.stop()
                client = Groq(api_key=api_key)
                analysis = analyse_resume(resume_text, client)
            st.markdown(analysis)
        except Exception as error:
            st.error(f"Analysis failed: {error}")
