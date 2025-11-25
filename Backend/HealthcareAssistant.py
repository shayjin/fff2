# from strands import Agent
# from strands.models.gemini import GeminiModel
# import os
# import requests
# from dotenv import load_dotenv
# from typing import List, Dict, Any
# from FIHR import FHIRClient
# from answer_accuarcy import similarity_score
from agent import get_agent
from tools import stdio_mcp_client


# class HealthcareAssistant:
#     def __init__(self):
#         load_dotenv()

#         # Check if API key exists
#         api_key = os.getenv("GEMINI_API_KEY")
#         if not api_key:
#             print("Error: GEMINI_API_KEY not found in .env file")
#             exit(1)

#         model = GeminiModel(
#                 client_args={"api_key": os.getenv("GEMINI_API_KEY")},
#                 model_id="gemini-2.5-flash",
#                 params={"temperature": 0.15},  # Lower temperature for consistent test behavior
#             )
#         agent = Agent(model=model)

#         self.fhir_client = FHIRClient()
#         self.agent = agent
#         self.server = "hapi" 

#     def set_server(self, server: str):
#         if server.lower() in ["hapi", "smart"]:
#             self.server = server.lower()
#             return f"Server set to {self.server.upper()}"
#         else:
#             return "Invalid server. "

#     async def answer_medical_query(self, query: str, patient_id: str | None = None) -> dict:
#         try:
#             context = await self.gather_medical_context(patient_id) if patient_id else ""
#             prompt = f"""
#                 You are a healthcare assistant. Please answer the following medical query:

#                 {query}
                
#                 {context}
                
#                 Please provide a clear and accurate response based on the available information.
#                 If you're unsure about anything, please acknowledge the uncertainty.
#             """
#             response = self.agent(prompt)
#             answer = str(response)

#             if context:
#                 accuracy_score = similarity_score(answer, context)
#             else:
#                 accuracy_score = None

#             return {
#                 "answer": answer,
#                 "accuracy_score": accuracy_score,
#                 "context_summary": context[:1000]
#             }
        
#         except Exception as e:
#             return {"error": f"I apologize, but I encountered an error: {str(e)}"}

#     async def gather_medical_context(self, patient_id: str) -> str:
#         try:
#             if self.server == "smart":
#                 base_url = self.fhir_client.smart_base_url
#             else:
#                 base_url = self.fhir_client.hapi_base_url

#             endpoint = f"{base_url}/Patient/{patient_id}"
#             response = requests.get(endpoint)
#             patient_data = response.json()

#             conditions_endpoint = f"{base_url}/Condition?subject=Patient/{patient_id}"
#             conditions_response = requests.get(conditions_endpoint)
#             conditions = conditions_response.json().get('entry', [])
#             obs_endpoint = f"{base_url}/Observation?patient={patient_id}"
#             obs_response = requests.get(obs_endpoint)
#             obs = obs_response.json().get('entry', [])
#             context = f"""
#                 Available Patient Information:
#                 {self.format_patient_info(patient_data)}
                
#                 Current Medical Conditions:
#                 {self.format_conditions(conditions)}
                
#                 Recent Medical Observations:
#                 {self.format_observations(obs)}
#             """
#             return context
#         except Exception as e:
#             return f"Note: Could not retrieve complete patient information: {str(e)}"
            



#     def format_patient_info(self, patient: Dict[str, Any]) -> str:
#         info = []

#         if not patient:
#             return "No information available"
        
#         if patient.get("name"):
#             name = patient["name"][0]
#             full_name = f"{' '.join(name.get('given', ['']))} {name.get('family', '')}"
#             info.append(f"Name: {full_name.strip()}")
        
#         if patient.get("gender"):
#             info.append(f"Gender: {patient['gender']}")
            
#         if patient.get("birthDate"):
#             info.append(f"Birth Date: {patient['birthDate']}")
            
#         return "\n".join(info) if info else "No information available"
    
#     def format_conditions(self, conditions: List[Dict[str, Any]]) -> str:   
#         formatted = []

#         if not conditions:
#             return "No information recorded"

#         for entry in conditions:
#             condition = entry.get('resource', {})

#             if condition.get("code", {}).get("coding"):
#                 code = condition["code"]["coding"][0]
#                 display = code.get("display", code.get("code", "Unknown condition"))
#                 status = condition.get("clinicalStatus", {}).get("coding", [{}])[0].get("code", "unknown")
#                 onset = condition.get("onsetDateTime", "unknown date")
                
#                 formatted.append(f"- {display} (Status: {status}, Onset: {onset})")
                
#                 if condition.get("evidence"):
#                     for evidence in condition["evidence"]:
#                         if evidence.get("detail"):
#                             formatted.append("  Evidence:")
#                             for detail in evidence["detail"]:
#                                 formatted.append(f"    - {detail.get('reference', 'No reference')}")
                
#         return "\n".join(formatted) if formatted else "No information recorded"

#     def format_observations(self, observations: List[Dict[str, Any]]) -> str:
#         if not observations:
#             return "No observations recorded"
            
#         formatted = []

#         for entry in observations:
#             obs = entry.get('resource', {})

#             if obs.get("code", {}).get("text"):
#                 if obs.get("valueQuantity"):
#                     value = obs["valueQuantity"]
#                     formatted.append(f"- {obs['code']['text']}: {value.get('value')} {value.get('unit', '')}")
#                 elif obs.get("valueCodeableConcept"):
#                     formatted.append(f"- {obs['code']['text']}: {obs['valueCodeableConcept'].get('text', 'No value')}")
#                 elif obs.get("valueString"):
#                     formatted.append(f"- {obs['code']['text']}: {obs['valueString']}")
                    
#         return "\n".join(formatted) if formatted else "No observations recorded"


class HealthcareAssistant:
    def __init__(self):
        self.mcp_client = stdio_mcp_client
        self.server = "smart"

    def set_server(self, server: str):
        if server.lower() in ["hapi", "smart"]:
            self.server = server.lower()
            return f"Server set to {self.server.upper()}"
        else:
            return "Invalid server."

    async def answer_medical_query(self, query: str, patient_id: str | None = None) -> dict:
        try:
            with self.mcp_client:
                agent = get_agent(self.mcp_client.list_tools_sync())
                
                if patient_id:
                    prompt = f"""You are a healthcare assistant. Answer this medical query for patient {patient_id}: {query}
                    
                    Use the available FHIR tools to gather relevant patient information before answering.
                    
                    Please provide a clear and accurate response based on the available information.
                    If you're unsure about anything, please acknowledge the uncertainty."""
                else:
                    prompt = f"""You are a healthcare assistant. Answer this medical query: {query}
                    
                    Please provide a clear and accurate response based on the available information.
                    If you're unsure about anything, please acknowledge the uncertainty."""
                
                response = agent(prompt)
                answer = str(response)
                
                return {"answer": answer}
        
        except Exception as e:
            return {"error": f"I apologize, but I encountered an error: {str(e)}"}