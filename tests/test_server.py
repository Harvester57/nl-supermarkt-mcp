"""Tests for NL Supermarkt MCP Server"""

import pytest
from src.server import server, list_tools, cli_main
import src.server_sse as server_sse


def test_server_metadata():
    """Verify MCP server is initialized with proper metadata."""
    assert server.name == "nl-supermarkt-mcp"
    assert callable(cli_main)
    assert callable(server_sse.main)


@pytest.mark.asyncio
async def test_server_tools_registration():
    """Verify all expected MCP tools are registered with schemas."""
    tools = await list_tools()
    assert len(tools) >= 5

    tool_names = {tool.name for tool in tools}
    expected_tools = {
        "zoek_producten",
        "vergelijk_prijzen",
        "optimaliseer_boodschappenlijst",
        "lijst_supermarkten",
        "lijst_drogisten",
        "zoek_recepten",
        "plan_boodschappen",
        "prijshistorie",
    }
    for expected in expected_tools:
        assert expected in tool_names, f"Missing tool: {expected}"

    for tool in tools:
        assert tool.name, "Tool must have a non-empty name"
        assert tool.description, f"Tool {tool.name} must have a description"
        assert isinstance(tool.inputSchema, dict), f"Tool {tool.name} must have an inputSchema dict"
