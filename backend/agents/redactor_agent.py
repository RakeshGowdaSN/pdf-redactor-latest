# backend/agents/redactor_agent.py
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
Redact the following text. Replace all values listed below with '{placeholder}'.

Fields to redact:
{fields}

Text:
---
{text}
---

Return the redacted text ONLY.
""")

chain = LLMChain(llm=llm, prompt=prompt)

def redact_text_with_llm(text: str, pii_fields: dict, placeholder: str = "[REDACTED]") -> str:
    try:
        return chain.run(text=text, fields=json.dumps(pii_fields), placeholder=placeholder)
    except Exception as e:
        print("Redaction LLM failed:", e)
        return text
