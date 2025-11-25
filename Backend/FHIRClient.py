import requests
import json

## Testing 3209597

class FHIRClient:
    """FHIR client that connects to local Docker HAPI server"""
    
    def __init__(self, base_url=None):
        self.base_url = base_url or "https://launch.smarthealthit.org/v/r4/fhir"

    # PATIENT CRUD
    def create_patient(self, given_name, family_name, gender=None, birth_date=None):
        """Create a new patient"""
        patient_data = {
            "resourceType": "Patient",
            "name": [{"family": family_name, "given": [given_name]}]
        }
        
        # Add optional fields only if provided
        if gender:
            patient_data["gender"] = gender.lower()
        if birth_date:
            patient_data["birthDate"] = birth_date
            
        try:
            response = requests.post(f"{self.base_url}/Patient", json=patient_data)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    def list_patients(self, count=10):
        """List patients from FHIR server"""
        try:
            response = requests.get(f"{self.base_url}/Patient?_count={count}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    def get_patient(self, patient_id):
        """Get specific patient by ID"""
        try:
            response = requests.get(f"{self.base_url}/Patient/{patient_id}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    def update_patient(self, patient_id, patient_data):
        """Update existing patient"""
        try:
            response = requests.put(f"{self.base_url}/Patient/{patient_id}", json=patient_data)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    def delete_patient(self, patient_id):
        """Delete patient"""
        try:
            response = requests.delete(f"{self.base_url}/Patient/{patient_id}")
            response.raise_for_status()
            return {"success": True}
        except Exception as e:
            return {"error": str(e)}

    # CONDITION CRUD
    def create_condition(self, condition_data):
        """Create a condition with complete FHIR R4 JSON structure
        
        FHIR R4 Condition structure (https://hl7.org/fhir/R4/condition.html):
        
        Nested structures:
        - Coding: { "system": "uri", "code": "string", "display": "string" }
        - CodeableConcept: { "coding": [Coding], "text": "string" }
        - Reference: { "reference": "string", "display": "string" }
        - Age: { "value": decimal, "unit": "string", "system": "uri", "code": "string" }
        - Period: { "start": "dateTime", "end": "dateTime" }
        - Range: { "low": Quantity, "high": Quantity }
        
        Full Condition structure:
        {
            "resourceType": "Condition",
            "id": "string",
            "meta": Meta,
            "implicitRules": "uri",
            "language": "code",
            "text": Narrative,
            "contained": [Resource],
            "extension": [Extension],
            "modifierExtension": [Extension],
            "identifier": [Identifier],
            "clinicalStatus": CodeableConcept,
            "verificationStatus": CodeableConcept,
            "category": [CodeableConcept],
            "severity": CodeableConcept,
            "code": CodeableConcept,
            "bodySite": [CodeableConcept],
            "subject": Reference,
            "encounter": Reference,
            "onsetDateTime": "dateTime",
            "onsetAge": Age,
            "onsetPeriod": Period,
            "onsetRange": Range,
            "onsetString": "string",
            "abatementDateTime": "dateTime",
            "abatementAge": Age,
            "abatementPeriod": Period,
            "abatementRange": Range,
            "abatementString": "string",
            "recordedDate": "dateTime",
            "recorder": Reference,
            "asserter": Reference,
            "stage": [{ "summary": CodeableConcept, "assessment": [Reference], "type": CodeableConcept }],
            "evidence": [{ "code": [CodeableConcept], "detail": [Reference] }],
            "note": [Annotation]
        }
        
        Minimum required: resourceType, subject
        """
        try:
            response = requests.post(f"{self.base_url}/Condition", json=condition_data)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    def get_patient_conditions(self, patient_id):
        """Get conditions for a specific patient"""
        try:
            response = requests.get(f"{self.base_url}/Condition?patient={patient_id}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    def update_condition(self, condition_id, condition_data):
        """Update existing condition with complete FHIR R4 JSON structure
        
        Uses same FHIR R4 Condition structure as create_condition.
        See create_condition method for complete structure details.
        Minimum required: resourceType, subject
        """
        try:
            response = requests.put(f"{self.base_url}/Condition/{condition_id}", json=condition_data)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    def delete_condition(self, condition_id):
        """Delete condition"""
        try:
            response = requests.delete(f"{self.base_url}/Condition/{condition_id}")
            response.raise_for_status()
            return {"success": True}
        except Exception as e:
            return {"error": str(e)}

    # MEDICATION CRUD
    def create_medication(self, medication_data):
        """Create a medication request with complete FHIR R4 JSON structure
        
        FHIR R4 MedicationRequest structure (https://hl7.org/fhir/R4/medicationrequest.html):
        
        Nested structures:
        - Coding: { "system": "uri", "code": "string", "display": "string" }
        - CodeableConcept: { "coding": [Coding], "text": "string" }
        - Reference: { "reference": "string", "display": "string" }
        - Quantity: { "value": decimal, "unit": "string", "system": "uri", "code": "string" }
        - Duration: { "value": decimal, "unit": "string", "system": "uri", "code": "string" }
        - Period: { "start": "dateTime", "end": "dateTime" }
        - Timing: { "repeat": { "frequency": integer, "period": decimal, "periodUnit": "s|min|h|d|wk|mo|a" } }
        - Dosage: { "text": "string", "timing": Timing, "route": CodeableConcept, "doseAndRate": [{ "doseQuantity": Quantity }] }
        
        Full MedicationRequest structure:
        {
            "resourceType": "MedicationRequest",
            "id": "string",
            "meta": Meta,
            "implicitRules": "uri",
            "language": "code",
            "text": Narrative,
            "contained": [Resource],
            "extension": [Extension],
            "modifierExtension": [Extension],
            "identifier": [Identifier],
            "status": "active|on-hold|cancelled|completed|entered-in-error|stopped|draft|unknown",
            "statusReason": CodeableConcept,
            "intent": "proposal|plan|order|original-order|reflex-order|filler-order|instance-order|option",
            "category": [CodeableConcept],
            "priority": "routine|urgent|asap|stat",
            "doNotPerform": "boolean",
            "reportedBoolean": "boolean",
            "reportedReference": Reference,
            "medicationCodeableConcept": CodeableConcept,
            "medicationReference": Reference,
            "subject": Reference,
            "encounter": Reference,
            "supportingInformation": [Reference],
            "authoredOn": "dateTime",
            "requester": Reference,
            "performer": Reference,
            "performerType": CodeableConcept,
            "recorder": Reference,
            "reasonCode": [CodeableConcept],
            "reasonReference": [Reference],
            "instantiatesCanonical": ["canonical"],
            "instantiatesUri": ["uri"],
            "basedOn": [Reference],
            "groupIdentifier": Identifier,
            "courseOfTherapyType": CodeableConcept,
            "insurance": [Reference],
            "note": [Annotation],
            "dosageInstruction": [Dosage],
            "dispenseRequest": {
                "initialFill": { "quantity": Quantity, "duration": Duration },
                "dispenseInterval": Duration,
                "validityPeriod": Period,
                "numberOfRepeatsAllowed": "unsignedInt",
                "quantity": Quantity,
                "expectedSupplyDuration": Duration,
                "performer": Reference
            },
            "substitution": {
                "allowedBoolean": "boolean",
                "allowedCodeableConcept": CodeableConcept,
                "reason": CodeableConcept
            },
            "priorPrescription": Reference,
            "detectedIssue": [Reference],
            "eventHistory": [Reference]
        }
        
        Minimum required: resourceType, status, intent, medicationCodeableConcept OR medicationReference, subject
        """
        try:
            response = requests.post(f"{self.base_url}/MedicationRequest", json=medication_data)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    def get_patient_medications(self, patient_id):
        """Get medications for a specific patient"""
        try:
            response = requests.get(f"{self.base_url}/MedicationRequest?patient={patient_id}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    def update_medication(self, medication_id, medication_data):
        """Update existing medication request with complete FHIR R4 JSON structure
        
        Uses same FHIR R4 MedicationRequest structure as create_medication.
        See create_medication method for complete structure details.
        Minimum required: resourceType, status, intent, medicationCodeableConcept OR medicationReference, subject
        """
        try:
            response = requests.put(f"{self.base_url}/MedicationRequest/{medication_id}", json=medication_data)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    def delete_medication(self, medication_id):
        """Delete medication"""
        try:
            response = requests.delete(f"{self.base_url}/MedicationRequest/{medication_id}")
            response.raise_for_status()
            return {"success": True}
        except Exception as e:
            return {"error": str(e)}

    # OBSERVATION CRUD
    def create_observation(self, observation_data):
        """Create an observation with complete FHIR R4 JSON structure
        
        FHIR R4 Observation structure with nested object definitions:
        
        Coding structure: { "system": "uri", "version": "string", "code": "string", "display": "string", "userSelected": "boolean" }
        CodeableConcept: { "coding": [Coding], "text": "string" }
        Reference: { "reference": "string", "type": "uri", "identifier": {}, "display": "string" }
        Quantity: { "value": "decimal", "comparator": "<|<=|>=|>", "unit": "string", "system": "uri", "code": "string" }
        Period: { "start": "dateTime", "end": "dateTime" }
        Range: { "low": Quantity, "high": Quantity }
        Ratio: { "numerator": Quantity, "denominator": Quantity }
        Identifier: { "use": "usual|official|temp|secondary|old", "type": CodeableConcept, "system": "uri", "value": "string", "period": Period }
        Annotation: { "authorReference": Reference, "authorString": "string", "time": "dateTime", "text": "markdown" }
        
        Full Observation structure:
        {
            "resourceType": "Observation",
            "id": "string",
            "meta": { "versionId": "string", "lastUpdated": "instant", "source": "uri", "profile": ["canonical"], "security": [Coding], "tag": [Coding] },
            "implicitRules": "uri",
            "language": "code",
            "text": { "status": "generated|extensions|additional|empty", "div": "xhtml" },
            "contained": [Resource],
            "extension": [Extension],
            "modifierExtension": [Extension],
            "identifier": [Identifier],
            "basedOn": [Reference],
            "partOf": [Reference],
            "status": "registered|preliminary|final|amended|corrected|cancelled|entered-in-error|unknown",
            "category": [CodeableConcept],
            "code": CodeableConcept,
            "subject": Reference,
            "focus": [Reference],
            "encounter": Reference,
            "effectiveDateTime": "dateTime",
            "effectivePeriod": Period,
            "effectiveTiming": Timing,
            "effectiveInstant": "instant",
            "issued": "instant",
            "performer": [Reference],
            "valueQuantity": Quantity,
            "valueCodeableConcept": CodeableConcept,
            "valueString": "string",
            "valueBoolean": "boolean",
            "valueInteger": "integer",
            "valueRange": Range,
            "valueRatio": Ratio,
            "valueSampledData": SampledData,
            "valueTime": "time",
            "valueDateTime": "dateTime",
            "valuePeriod": Period,
            "dataAbsentReason": CodeableConcept,
            "interpretation": [CodeableConcept],
            "note": [Annotation],
            "bodySite": CodeableConcept,
            "method": CodeableConcept,
            "specimen": Reference,
            "device": Reference,
            "referenceRange": [{ "low": Quantity, "high": Quantity, "type": CodeableConcept, "appliesTo": [CodeableConcept], "age": Range, "text": "string" }],
            "hasMember": [Reference],
            "derivedFrom": [Reference],
            "component": [{ "code": CodeableConcept, "valueQuantity": Quantity, "valueCodeableConcept": CodeableConcept, "valueString": "string", "valueBoolean": "boolean", "valueInteger": "integer", "valueRange": Range, "valueRatio": Ratio, "valueSampledData": SampledData, "valueTime": "time", "valueDateTime": "dateTime", "valuePeriod": Period, "dataAbsentReason": CodeableConcept, "interpretation": [CodeableConcept], "referenceRange": [ReferenceRange] }]
        }
        
        Minimum required: resourceType, status, code, subject
        """
        try:
            response = requests.post(f"{self.base_url}/Observation", json=observation_data)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    def get_patient_observations(self, patient_id):
        """Get observations for a specific patient"""
        try:
            response = requests.get(f"{self.base_url}/Observation?patient={patient_id}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    def update_observation(self, observation_id, observation_data):
        """Update existing observation with complete FHIR R4 JSON structure
        
        Uses same FHIR R4 Observation structure as create_observation:
        
        Nested structures:
        - Coding: { "system": "uri", "code": "string", "display": "string" }
        - CodeableConcept: { "coding": [Coding], "text": "string" }
        - Reference: { "reference": "string", "display": "string" }
        - Quantity: { "value": decimal, "unit": "string", "system": "uri", "code": "string" }
        
        Full structure same as create_observation - see that method for complete details.
        Must include resourceType, status, code, subject at minimum.
        """
        try:
            response = requests.put(f"{self.base_url}/Observation/{observation_id}", json=observation_data)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    def delete_observation(self, observation_id):
        """Delete observation"""
        try:
            response = requests.delete(f"{self.base_url}/Observation/{observation_id}")
            response.raise_for_status()
            return {"success": True}
        except Exception as e:
            return {"error": str(e)}

    def get_patient_summary(self, patient_id):
        """Get complete patient summary"""
        patient = self.get_patient(patient_id)
        conditions = self.get_patient_conditions(patient_id)
        medications = self.get_patient_medications(patient_id)
        observations = self.get_patient_observations(patient_id)
        
        return {
            "patient": patient,
            "conditions": conditions,
            "medications": medications,
            "observations": observations
        }