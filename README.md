
# GenAI-Powered PDF Redactor Web App (GCP Hosted)

This is a production-ready, GenAI-powered redaction application that automates secure removal of sensitive content from PDFs using agentic intelligence — with LLMs, OCR, and CrewAI orchestration. Designed for large-scale enterprise redaction workflows.

---

## Features

- Bulk PDF uploads
- Redaction via LLM agents (emails, SSNs, phones, names)
- Manual redaction override support (via planned React UI)
- Page-range-based redaction
- Placeholder insertion (`[REDACTED]`)
- OCR-based logo/image redaction (Tesseract / Google Vision)
- Secure downloads via signed GCS URLs
- Stateless, horizontally scalable backend on GCP Cloud Run

---

## Project Structure

```
pdf-redactor-app/
├── backend/ # FastAPI + CrewAI Agentic Backend
│ ├── agents/ # LLM, OCR, Redactor agent logic
│ │ ├── inspector_agent.py
│ │ ├── redactor_agent.py
│ │ └── ocr_agent.py
│ ├── crew/ # CrewAI setup and orchestration
│ │ └── crew_setup.py
│ ├── utils/ # PDF parsing, text extraction
│ │ └── pdf_utils.py
│ ├── main.py # FastAPI endpoints (upload, redact, preview)
│ ├── requirements.txt
│ └── Dockerfile
├── frontend/ # ReactJS UI (upload + preview)
│ ├── src/
│ ├── public/
│ └── package.json
├── deployment/ # Infra setup scripts for GCP
│ ├── cloud_run_deploy.sh
│ └── setup_gcp.md
└── README.md
```

---

## Local Development

### Backend
```bash
cd backend
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

---

## GCP Deployment Instructions

### 1. Enable Required APIs
```bash
gcloud services enable \
  run.googleapis.com \
  redis.googleapis.com \
  vision.googleapis.com \
  secretmanager.googleapis.com \
  artifactregistry.googleapis.com
```

### 2. IAM & Networking
```bash
gcloud compute networks create redactor-vpc --subnet-mode=custom
```
Assign roles:
    - roles/cloudrun.admin
    - roles/secretmanager.secretAccessor
    - roles/storage.admin
    - roles/logging.viewer

### 3. Artifact Registry & Build
```bash
gcloud artifacts repositories create redactor-repo \
  --repository-format=docker \
  --location=us-central1

gcloud builds submit \
  --tag us-central1-docker.pkg.dev/YOUR_PROJECT_ID/redactor-repo/agentic-redactor
```

### 4. Deploy to Cloud Run
```bash
gcloud run deploy redactor-service \
  --image us-central1-docker.pkg.dev/YOUR_PROJECT_ID/redactor-repo/agentic-redactor \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### 5. Frontend Hosting on GCS
```bash
npm run build
gsutil -m cp -r build/* gs://pdf-redactor-ui/
gsutil web set -m index.html -e 404.html gs://pdf-redactor-ui/
```

---

## Security Considerations

- Signed GCS URLs with expiry for secure downloads
- Google IAM used for least-privilege agent roles
- All secrets managed via Secret Manager

---

## Monitoring

- Google Cloud Logging (Logs Explorer)
- Monitoring dashboard + alerting via Cloud Monitoring

---

## Technologies Used

| Layer         | Tech Stack                              |
|---------------|-----------------------------------------|
| Backend       | FastAPI, PyMuPDF, CrewAI, Langchain     |
| Orchestration | CrewAI / LangGraph / Google ADK         |
| LLM           | OpenAI GPT-4, Gemini                    |
| OCR           | PyMuPDF + Tesseract / Google Vision API |
| Frontend      | ReactJS, Axios, Bootstrap               |
| Hosting       | GCP Cloud Run (Docker)                  |
| Storage       | GCS (Google Cloud Storage)              |
| Memory        | Redis via GCP Memorystore               |
| Monitoring    | Cloud Logging & Monitoring              |

---

## Agentic Redaction Flow
1) OCR Agent (optional): Extracts text from scanned pages
2) Inspector Agent: Detects PII fields via LLM (detect_pii_with_llm)
3) Redactor Agent: Replaces PII content via LLM (redact_text_with_llm)
4) CrewAI Orchestration: Ensures task coordination and output
    Toggle use_ocr=True in the API to handle image-based PDFs

---

## Future Enhancements

| Feature                    | Benefit                          |
|----------------------------|----------------------------------|
| OAuth / SSO login          | Secure enterprise authentication |
| React-based annotation UI  | Manual redaction precision       |
| LLM Embedding Classifier   | Smarter redaction than regex     |
| Async Workers via Pub/Sub  | Support huge file redactions     |
| Audit Logs + RLHF Feedback | Compliance + Agent fine-tuning   |
| Multi-language Redaction   | Multilingual document support    |

---

## Contributions

This redactor app is modular by design — feel free to contribute your own:
    - PII agent modules
    - Document format handlers
    - Frontend annotation layers
    - Backend task queue integrations

Built for enterprise-grade secure document handling using GenAI workflows.
