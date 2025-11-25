import sys
import os
import asyncio
import io
from contextlib import redirect_stdout
sys.path.append(os.path.join(os.path.dirname(__file__), 'Backend'))

from agent import get_agent
from tools import stdio_mcp_client

async def main():

    with stdio_mcp_client:
        agent = get_agent(stdio_mcp_client.list_tools_sync())

        print("FHIR Medical Assistant CLI")
        print("Type 'quit' or 'exit' to end the session\n")

        while True:
            try:
                user_input = input("You: ").strip()

                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("Goodbye!")
                    break

                if not user_input:
                    continue

                # Capture stdout to prevent agent from printing during execution
                captured_output = io.StringIO()
                with redirect_stdout(captured_output):
                    response = agent(user_input)
                
                print("Assistant: ", end="", flush=True)
                print(str(response))
                
                # # Extract text from AgentResult
                # if hasattr(response, 'message') and 'content' in response.message:
                #     content = response.message['content']
                #     if content and isinstance(content, list) and len(content) > 0:
                #         text = content[0].get('text', '')
                #         print(text.strip())
                #     else:
                #         print("No response content")
                # else:
                #     print(str(response))
                print()

            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")
                print()

if __name__ == "__main__":
    asyncio.run(main())