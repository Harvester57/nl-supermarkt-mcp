"""Tests for NL Supermarkt MCP Server"""

import pytest
import mcp.types as types
from src.server import server, list_tools, call_tool, cli_main
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
        schema = getattr(tool, "input_schema", None) or getattr(tool, "inputSchema", None)
        assert isinstance(schema, dict), f"Tool {tool.name} must have an input schema dict"


@pytest.mark.asyncio
async def test_call_tool_unknown():
    """Verify calling an unknown tool returns a TextContent response without unhandled crash."""
    result = await call_tool("nonexistent_tool", {})
    assert isinstance(result, list)
    assert len(result) > 0
    assert hasattr(result[0], "text")
    assert len(result[0].text) > 0


@pytest.mark.asyncio
async def test_server_request_handlers():
    """Verify protocol request handlers are registered on the server instance."""
    if hasattr(server, "get_request_handler"):
        # MCP 2.x request handlers
        list_entry = server.get_request_handler("tools/list")
        assert list_entry is not None
        params = types.PaginatedRequestParams()
        list_res = await list_entry.handler(None, params)
        assert len(list_res.tools) >= 5

        call_entry = server.get_request_handler("tools/call")
        assert call_entry is not None
        call_params = types.CallToolRequestParams(name="nonexistent_tool", arguments={})
        call_res = await call_entry.handler(None, call_params)
        assert isinstance(call_res, types.CallToolResult)
        assert len(call_res.content) > 0
