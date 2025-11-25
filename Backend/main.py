from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import sys
import os
from HealthcareAssistant import HealthcareAssistant
import uvicorn

sys.path.append(os.path.dirname(__file__))
app = FastAPI(title="AI Medical Assistant Chatbot API")

# Add CORS middleware to allow requests from Streamlit Cloud
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, you may want to restrict this to your Streamlit app URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

assistant = HealthcareAssistant()

class QueryRequest(BaseModel):
    query: str

class PatientRequest(BaseModel):
    patient_id: str

class ServerRequest(BaseModel):
    server: str

patient_id: Optional[str] = None

"""
    "/query": "POST - Ask a medical question",
    "/patient": "POST - Set patient ID",
    "/patient": "GET - Get current patient ID",
    "/patient": "DELETE - Clear patient ID",
    "/server": "POST - Set FHIR server (hapi or smart)",
    "/server": "GET - Get current FHIR server"
"""

@app.post("/ask")
async def ask(request: QueryRequest):
    """Ask the healthcare assistant a question"""

    try:
        result = await assistant.answer_medical_query(request.query, patient_id)
        return {
            "query": request.query,
            "patient_id": patient_id,
            **result,
            "server": assistant.server
        }
    except Exception as e:
        return {"error": str(e)}

@app.post("/patient")
async def set_patient(request: PatientRequest):
    """Set the patient ID for queries"""
    
    global patient_id
    patient_id = request.patient_id

    return {
        "message": f"Patient ID set to {patient_id}",
        "patient_id": patient_id
    }

@app.get("/patient")
async def get_patient():
    """Get the current patient ID"""

    return {
        "patient_id": patient_id
    }

@app.delete("/patient")
async def clear_patient():
    """Clear the current patient ID"""

    global patient_id
    patient_id = None

    return {
        "message": "Patient ID cleared",
        "patient_id": patient_id
    }

@app.post("/server")
async def set_server(request: ServerRequest):
    """Set the FHIR server (hapi or smart)"""

    result = assistant.set_server(request.server)

    return {
        "message": result,
        "current_server": assistant.server
    }

@app.get("/server")
async def get_server():
    """Get the current FHIR server"""
    
    return {
        "current_server": assistant.server
    }

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
