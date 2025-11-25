#!/usr/bin/env python3

import json
from mcp.server.fastmcp import FastMCP
from FHIRClient import FHIRClient

# Initialize FHIR client and MCP server
fhir_client = FHIRClient()
mcp = FastMCP("FHIR Medical Assistant")

# PATIENT TOOLS
@mcp.tool()
def create_patient(given_name: str, family_name: str, gender: str, birth_date: str) -> str:
    """Create a new patient record in the FHIR server with basic demographic information
    
    Args:
        given_name: Patient's first name
        family_name: Patient's last name
        gender: Patient's gender (male/female/other)
        birth_date: Patient's birth date in YYYY-MM-DD format
    """
    result = fhir_client.create_patient(given_name, family_name, gender, birth_date)
    return json.dumps(result, indent=2)

@mcp.tool()
def list_patients(count: int = 10) -> str:
    """Retrieve a list of patients from the FHIR server with their basic information
    
    Args:
        count: Maximum number of patients to return (default: 10, must be positive)
    """
    if count <= 0:
        return json.dumps({"error": "Count must be a positive integer"}, indent=2)
    result = fhir_client.list_patients(count)
    return json.dumps(result, indent=2)

@mcp.tool()
def get_patient(patient_id: str) -> str:
    """Retrieve detailed information for a specific patient using their unique ID
    
    Args:
        patient_id: Unique FHIR patient identifier
    """
    result = fhir_client.get_patient(patient_id)
    return json.dumps(result, indent=2)

@mcp.tool()
def delete_patient(patient_id: str) -> str:
    """Remove a patient record from the FHIR server using their unique ID
    
    Args:
        patient_id: Unique FHIR patient identifier to delete
    """
    result = fhir_client.delete_patient(patient_id)
    return json.dumps(result, indent=2)

# CONDITION TOOLS
@mcp.tool()
def create_condition(condition_json: str) -> str:
    """Create a new medical condition using complete FHIR R4 JSON structure
    
    Args:
        condition_json: Complete FHIR R4 Condition JSON string with nested structures:
        
        Key nested structures:
        - Coding: { "system": "uri", "code": "string", "display": "string" }
        - CodeableConcept: { "coding": [Coding], "text": "string" }
        - Reference: { "reference": "string", "display": "string" }
        
        Minimum required structure:
        {
            "resourceType": "Condition",
            "subject": { "reference": "Patient/123" },
            "code": { "text": "Diabetes" },
            "clinicalStatus": { "coding": [{ "system": "http://terminology.hl7.org/CodeSystem/condition-clinical", "code": "active" }] }
        }
        
        Full spec: https://hl7.org/fhir/R4/condition.html
    """
    try:
        condition_data = json.loads(condition_json)
        result = fhir_client.create_condition(condition_data)
        return json.dumps(result, indent=2)
    except json.JSONDecodeError:
        return json.dumps({"error": "Invalid JSON format"}, indent=2)

@mcp.tool()
def get_patient_conditions(patient_id: str) -> str:
    """Retrieve all medical conditions and diagnoses associated with a specific patient
    
    Args:
        patient_id: Unique FHIR patient identifier
    """
    result = fhir_client.get_patient_conditions(patient_id)
    return json.dumps(result, indent=2)

@mcp.tool()
def update_condition(condition_id: str, condition_json: str) -> str:
    """Update an existing medical condition using complete FHIR R4 JSON structure
    
    Args:
        condition_id: Unique FHIR condition identifier to update
        condition_json: Complete FHIR R4 Condition JSON string with nested structures.
        Must include resourceType, subject at minimum.
        Full spec: https://hl7.org/fhir/R4/condition.html
    """
    try:
        condition_data = json.loads(condition_json)
        result = fhir_client.update_condition(condition_id, condition_data)
        return json.dumps(result, indent=2)
    except json.JSONDecodeError:
        return json.dumps({"error": "Invalid JSON format"}, indent=2)

@mcp.tool()
def delete_condition(condition_id: str) -> str:
    """Remove a specific medical condition from the FHIR server using its unique ID
    
    Args:
        condition_id: Unique FHIR condition identifier to delete
    """
    result = fhir_client.delete_condition(condition_id)
    return json.dumps(result, indent=2)

# MEDICATION TOOLS
@mcp.tool()
def create_medication(medication_json: str) -> str:
    """Create a new medication request using complete FHIR R4 JSON structure
    
    Args:
        medication_json: Complete FHIR R4 MedicationRequest JSON string with nested structures:
        
        Key nested structures:
        - Coding: { "system": "uri", "code": "string", "display": "string" }
        - CodeableConcept: { "coding": [Coding], "text": "string" }
        - Reference: { "reference": "string", "display": "string" }
        - Dosage: { "text": "string", "timing": {}, "route": CodeableConcept }
        
        Minimum required structure:
        {
            "resourceType": "MedicationRequest",
            "status": "active",
            "intent": "order",
            "medicationCodeableConcept": { "text": "Aspirin" },
            "subject": { "reference": "Patient/123" }
        }
        
        Full spec: https://hl7.org/fhir/R4/medicationrequest.html
    """
    try:
        medication_data = json.loads(medication_json)
        result = fhir_client.create_medication(medication_data)
        return json.dumps(result, indent=2)
    except json.JSONDecodeError:
        return json.dumps({"error": "Invalid JSON format"}, indent=2)

@mcp.tool()
def get_patient_medications(patient_id: str) -> str:
    """Retrieve all medication prescriptions and requests for a specific patient
    
    Args:
        patient_id: Unique FHIR patient identifier
    """
    result = fhir_client.get_patient_medications(patient_id)
    return json.dumps(result, indent=2)

@mcp.tool()
def update_medication(medication_id: str, medication_json: str) -> str:
    """Update an existing medication request using complete FHIR R4 JSON structure
    
    Args:
        medication_id: Unique FHIR medication request identifier to update
        medication_json: Complete FHIR R4 MedicationRequest JSON string with nested structures.
        Must include resourceType, status, intent, medicationCodeableConcept OR medicationReference, subject.
        Full spec: https://hl7.org/fhir/R4/medicationrequest.html
    """
    try:
        medication_data = json.loads(medication_json)
        result = fhir_client.update_medication(medication_id, medication_data)
        return json.dumps(result, indent=2)
    except json.JSONDecodeError:
        return json.dumps({"error": "Invalid JSON format"}, indent=2)

@mcp.tool()
def delete_medication(medication_id: str) -> str:
    """Remove a specific medication prescription from the FHIR server using its unique ID
    
    Args:
        medication_id: Unique FHIR medication request identifier to delete
    """
    result = fhir_client.delete_medication(medication_id)
    return json.dumps(result, indent=2)

# OBSERVATION TOOLS
@mcp.tool()
def create_observation(observation_json: str) -> str:
    """Create a new clinical observation using complete FHIR R4 JSON structure
    
    Args:
        observation_json: Complete FHIR R4 Observation JSON string with nested structures:
        
        Key nested structures:
        - Coding: { "system": "uri", "code": "string", "display": "string" }
        - CodeableConcept: { "coding": [Coding], "text": "string" }
        - Reference: { "reference": "string", "display": "string" }
        - Quantity: { "value": decimal, "unit": "string", "system": "uri", "code": "string" }
        
        Minimum required structure:
        {
            "resourceType": "Observation",
            "status": "final",
            "code": { 
                "coding": [{ "system": "http://loinc.org", "code": "8310-5", "display": "Body temperature" }], 
                "text": "Body temperature" 
            },
            "subject": { "reference": "Patient/123" }
        }
        
        Add value using one of: valueQuantity, valueString, valueBoolean, valueInteger, etc.
        Full spec: https://hl7.org/fhir/R4/observation.html
    """
    try:
        observation_data = json.loads(observation_json)
        result = fhir_client.create_observation(observation_data)
        return json.dumps(result, indent=2)
    except json.JSONDecodeError:
        return json.dumps({"error": "Invalid JSON format"}, indent=2)

@mcp.tool()
def get_patient_observations(patient_id: str) -> str:
    """Retrieve all clinical observations and measurements for a specific patient
    
    Args:
        patient_id: Unique FHIR patient identifier
    """
    result = fhir_client.get_patient_observations(patient_id)
    return json.dumps(result, indent=2)

@mcp.tool()
def update_observation(observation_id: str, observation_json: str) -> str:
    """Update an existing clinical observation using complete FHIR R4 JSON structure
    
    Args:
        observation_id: Unique FHIR observation identifier to update
        observation_json: Complete FHIR R4 Observation JSON string with nested structures:
        
        Key nested structures:
        - Coding: { "system": "uri", "code": "string", "display": "string" }
        - CodeableConcept: { "coding": [Coding], "text": "string" }
        - Reference: { "reference": "string", "display": "string" }
        - Quantity: { "value": decimal, "unit": "string", "system": "uri", "code": "string" }
        
        Must include resourceType, status, code, subject at minimum.
        Full spec: https://hl7.org/fhir/R4/observation.html
    """
    try:
        observation_data = json.loads(observation_json)
        result = fhir_client.update_observation(observation_id, observation_data)
        return json.dumps(result, indent=2)
    except json.JSONDecodeError:
        return json.dumps({"error": "Invalid JSON format"}, indent=2)

@mcp.tool()
def delete_observation(observation_id: str) -> str:
    """Remove a specific clinical observation from the FHIR server using its unique ID
    
    Args:
        observation_id: Unique FHIR observation identifier to delete
    """
    result = fhir_client.delete_observation(observation_id)
    return json.dumps(result, indent=2)

# SUMMARY TOOL
@mcp.tool()
def get_patient_summary(patient_id: str) -> str:
    """Generate a comprehensive patient summary including demographics, conditions, medications, and observations
    
    Args:
        patient_id: Unique FHIR patient identifier
    """
    result = fhir_client.get_patient_summary(patient_id)
    return json.dumps(result, indent=2) 

if __name__ == "__main__":
    # Initialize and run the server
    print("starting server")
    mcp.run(transport='stdio')