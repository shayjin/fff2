import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'Backend'))

from HealthcareAssistant import HealthcareAssistant
import asyncio

async def main():
    assistant = HealthcareAssistant()
    current_patient_id = None
    
    print("FHIR Medical Assistant CLI")
    print("Commands:")
    print("  /server <server name> - Set the FHIR server (hapi or smart)")
    print("  /patient <id> - Set patient ID for queries")
    print("  /clear - Clear current patient ID")
    print("  /help - Show these commands")
    print("  quit or exit - End the session")
    print("\nCurrent mode: General\n")
    print("\nCurrnet server: HAPI")
    print()

    # Use 50866993 for HAPI server testing
    # Use 6579753c-cb57-4962-a417-a0478b1115aa for SMART server testing
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
                
            if not user_input:
                continue
            
            if user_input.startswith('/'):
                parts = user_input.split()
                command = parts[0].lower()
                
                if command == '/patient':
                    if len(parts) > 1:
                        current_patient_id = parts[1]
                        print(f"\nNow querying for patient ID: {current_patient_id}")
                        print("Mode: Patient-specific queries")
                        print(f"Server: {assistant.server.upper()}\n")
                    else:
                        print("Please provide a patient ID (e.g., /patient 50866993)")

                    continue
                    
                elif command == '/clear':
                    current_patient_id = None
                    print("\nCleared patient ID")
                    print("Mode: General\n")
                    print(f"Server: {assistant.server.upper()}")
                    continue
                    
                elif command == '/help':
                    print("\nCommands:")
                    print("  /patient <id> - Set patient ID for queries")
                    print("  /clear - Clear current patient ID")
                    print("  /help - Show these commands")
                    print("  quit or exit - End the session")
                    print(f"\nCurrent mode: {'Patient-specific queries for ID: ' + current_patient_id if current_patient_id else 'General'}\n")
                    print(f"\nCurrent server: {assistant.server.upper()}\n")
                    continue
                    

                elif command == '/server':
                    if len(parts) > 1:
                        result = assistant.set_server(parts[1])
                        print(f"\n{result}\n")
                    else:
                        print("Please specify a server: hapi or smart (e.g., /server smart)")
                    continue
                else:
                    print(f"Unknown command: {command}")
                    continue

            print("Assistant: ", end="", flush=True)
            response = await assistant.answer_medical_query(user_input, current_patient_id)
            print()
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")
            print()

if __name__ == "__main__":
    asyncio.run(main())