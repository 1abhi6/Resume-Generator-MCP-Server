from fastmcp import FastMCP

mcp = FastMCP("ResuForge MCP Server")


@mcp.tool
def generate_resume(input_text: str) -> dict:
    """
    Accepts free-text or structured user input and returns a placeholder response.
    Replace body with actual parsing, LLM, and resume logic.
    """
    # For now, just echo back the input as a dict
    return {"message": "Received input", "input": input_text}


if __name__ == "__main__":
    mcp.run()
