# Deployment Guide for Google Cloud Run

This guide provides instructions on how to deploy the Multi-Source AI Copilot to Google Cloud Run.

## Prerequisites

- A Google Cloud Platform (GCP) project.
- The `gcloud` CLI installed and configured.
- Docker installed.

## Backend Deployment (FastAPI)

### 1. Create a Dockerfile

Create a `Dockerfile` in the `backend` directory with the following content:

```Dockerfile
# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip --no-cache-dir -r requirements.txt

# Copy the rest of the backend code to the working directory
COPY . .

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
```

### 2. Build the Docker Image

Navigate to the `backend` directory and build the Docker image:

```bash
# Replace [PROJECT_ID] with your GCP project ID
# Replace [IMAGE_NAME] with your desired image name
export PROJECT_ID="[PROJECT_ID]"
export IMAGE_NAME="ai-copilot-backend"

docker build -t gcr.io/${PROJECT_ID}/${IMAGE_NAME}:latest .
```

### 3. Push the Image to Google Container Registry (GCR)

```bash
docker push gcr.io/${PROJECT_ID}/${IMAGE_NAME}:latest
```

### 4. Deploy to Cloud Run

```bash
gcloud run deploy ${IMAGE_NAME} \
  --image gcr.io/${PROJECT_ID}/${IMAGE_NAME}:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
```

This command will deploy the backend to Cloud Run and provide you with a URL.

## Frontend Deployment (React)

The React frontend can be deployed to any static hosting service like Firebase Hosting, Netlify, or Vercel.

### 1. Build the Frontend

Navigate to the `frontend` directory and build the static files:

```bash
npm run build
```

This will create a `build` directory with the optimized static files.

### 2. Deploy to Firebase Hosting (Example)

1.  **Install Firebase CLI:**
    ```bash
    npm install -g firebase-tools
    ```

2.  **Initialize Firebase:**
    ```bash
    firebase login
    firebase init hosting
    ```
    - Select your GCP project.
    - Use the `build` directory as the public directory.
    - Configure as a single-page app (rewrite all urls to /index.html).

3.  **Deploy:**
    ```bash
    firebase deploy
    ```

### 3. Configure API Proxy

After deploying the backend, you need to update the frontend to use the Cloud Run URL.
- In `frontend/src/App.js`, replace the `/api/ask` and `/api/upload` endpoints with the full Cloud Run URL.
- Alternatively, you can use a proxy service or configure rewrites in your hosting provider to forward requests to the backend.
