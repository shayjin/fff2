from mcp import stdio_client, StdioServerParameters
from strands.tools.mcp import MCPClient

stdio_mcp_client = MCPClient(lambda: stdio_client(
    StdioServerParameters(
        command="uv",
        args=["run", "Backend/fhir_mcp_server.py"]
    )
))