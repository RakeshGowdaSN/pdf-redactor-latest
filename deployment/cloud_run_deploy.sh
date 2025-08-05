# deployment/cloud_run_deploy.sh

#!/bin/bash
PROJECT_ID=$(gcloud config get-value project)
REGION=us-central1
IMAGE=agentic-redactor

gcloud builds submit --tag ${REGION}-docker.pkg.dev/${PROJECT_ID}/redactor-repo/${IMAGE}
gcloud run deploy redactor-service \
  --image ${REGION}-docker.pkg.dev/${PROJECT_ID}/redactor-repo/${IMAGE} \
  --region ${REGION} \
  --platform managed \
  --allow-unauthenticated \
  --set-env-vars OPENAI_API_KEY=$OPENAI_API_KEY
