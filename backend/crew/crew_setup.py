# backend/crew/crew_setup.py

from crewai import Agent, Task, Crew
from agents.inspector_agent import detect_pii_with_llm
from agents.redactor_agent import redact_text_with_llm
from agents.ocr_agent import run_ocr_on_pdf
import os

# Define agents
inspector_agent = Agent(
    role="Inspector Agent",
    goal="Detect emails, SSNs, phones, and names",
    backstory="A redaction specialist AI trained to extract personal data.",
    allow_delegation=False,
    verbose=True
)

redactor_agent = Agent(
    role="Redactor Agent",
    goal="Redact all sensitive PII fields from the document.",
    backstory="An AI that replaces sensitive data with [REDACTED] while preserving context.",
    allow_delegation=False,
    verbose=True
)

# Optional: OCR Agent (Not crewai.Agent, just preprocessing step)
def run_crew(pdf_path: str, use_ocr: bool = False) -> str:
    """
    Runs the crew workflow on a PDF.
    If use_ocr is True, extracts text using OCR. Otherwise, use PyMuPDF.
    """
    if use_ocr:
        print("[INFO] Running OCR on PDF...")
        text = run_ocr_on_pdf(pdf_path)
    else:
        from utils.pdf_utils import extract_text_from_pdf
        text = extract_text_from_pdf(pdf_path)

    print("[INFO] Extracted text length:", len(text))

    # Define Tasks
    task1 = Task(
        description="Identify PII fields in the text.",
        expected_output="JSON list of PII fields",
        agent=inspector_agent,
        function=lambda: detect_pii_with_llm(text)
    )

    task2 = Task(
        description="Redact PII from text using placeholder.",
        expected_output="Clean redacted document",
        agent=redactor_agent,
        function=lambda: redact_text_with_llm(text, detect_pii_with_llm(text))
    )

    crew = Crew(
        agents=[inspector_agent, redactor_agent],
        tasks=[task1, task2],
        verbose=True
    )

    result = crew.kickoff()
    return result
