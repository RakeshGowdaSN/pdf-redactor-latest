# backend/agents/inspector_agent.py
import os
import json

from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chat_models import ChatOpenAI

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")

if LLM_PROVIDER == "openai":
    from langchain.chat_models import ChatOpenAI
    llm = ChatOpenAI(temperature=0, model_name="gpt-4", api_key=os.getenv("OPENAI_API_KEY"))
else:
    from langchain_google_genai import ChatGoogleGenerativeAI
    llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0, google_api_key=os.getenv("GEMINI_API_KEY"))

prompt = PromptTemplate.from_template("""
You are an information extraction agent.
Identify all sensitive personal information in the following text.

Return ONLY valid JSON in the format:
{{
    "emails": [...],
    "phones": [...],
    "ssns": [...],
    "names": [...]
}}

---
{text}
---
""")

chain = LLMChain(llm=llm, prompt=prompt)

def detect_pii_with_llm(text: str) -> dict:
    try:
        response = chain.run(text=text)
        pii_data = json.loads(response)
    except Exception as e:
        print("PII Detection failed:", e)
        pii_data = {"emails": [], "phones": [], "ssns": [], "names": []}
    return pii_data
