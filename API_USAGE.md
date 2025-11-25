# API Usage Guide

Your backend is deployed at: **https://s-aof7.onrender.com/**

## Quick Access

- **API Documentation (Swagger UI)**: https://s-aof7.onrender.com/docs
- **Alternative Docs (ReDoc)**: https://s-aof7.onrender.com/redoc

## Making Requests

### Using Python (requests library)

```python
import requests

API_BASE = "https://s-aof7.onrender.com"

# Set a patient ID
response = requests.post(
    f"{API_BASE}/patient",
    json={"patient_id": "patient-123"}
)
print(response.json())

# Ask a medical question
response = requests.post(
    f"{API_BASE}/ask",
    json={"query": "What medications am I taking?"},
    timeout=60
)
print(response.json())
```

### Using cURL

```bash
# Set patient ID
curl -X POST https://s-aof7.onrender.com/patient \
  -H "Content-Type: application/json" \
  -d '{"patient_id": "patient-123"}'

# Ask a question
curl -X POST https://s-aof7.onrender.com/ask \
  -H "Content-Type: application/json" \
  -d '{"query": "What is diabetes?"}'

# Get current patient ID
curl https://s-aof7.onrender.com/patient
```

### Using the API Documentation

1. Go to https://s-aof7.onrender.com/docs
2. Click on any endpoint (e.g., `/ask`)
3. Click "Try it out"
4. Fill in the request body
5. Click "Execute"
6. See the response below

## Available Endpoints

### POST /ask
Ask the healthcare assistant a medical question.

**Request Body:**
```json
{
  "query": "What medications am I taking?"
}
```

**Response:**
```json
{
  "query": "What medications am I taking?",
  "patient_id": "patient-123",
  "answer": "...",
  "server": "smart"
}
```

### POST /patient
Set the patient ID for subsequent queries.

**Request Body:**
```json
{
  "patient_id": "patient-123"
}
```

### GET /patient
Get the current patient ID.

**Response:**
```json
{
  "patient_id": "patient-123"
}
```

### DELETE /patient
Clear the current patient ID.

### POST /server
Set the FHIR server (hapi or smart).

**Request Body:**
```json
{
  "server": "smart"
}
```

### GET /server
Get the current FHIR server.

## Testing

Run the test script:
```bash
python test_api.py
```

This will test all endpoints and show you the responses.

## For Streamlit Frontend

Update your Streamlit Cloud secrets with:
```
API_BASE_URL=https://s-aof7.onrender.com
```

Then your Streamlit app will automatically use this backend URL!



