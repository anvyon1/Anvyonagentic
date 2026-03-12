"""Tests for ToolRegistry"""

import pytest
from anvyonagentic.tools import ToolRegistry


class TestToolRegistry:
    def test_list_tools(self):
        registry = ToolRegistry()
        tools = registry.list()
        assert len(tools) > 0

    def test_calculate(self):
        registry = ToolRegistry()
        result = registry.execute("calculate", {"expression": "2 + 3 * 4"})
        assert result["success"] is True
        assert result["data"]["result"] == 14

    def test_datetime(self):
        registry = ToolRegistry()
        result = registry.execute("datetime", {"format": "iso"})
        assert result["success"] is True
        assert "datetime" in result["data"]

    def test_text_transform_upper(self):
        registry = ToolRegistry()
        result = registry.execute("text_transform", {"text": "hello", "operation": "upper"})
        assert result["success"] is True
        assert result["data"]["result"] == "HELLO"

    def test_text_transform_lower(self):
        registry = ToolRegistry()
        result = registry.execute("text_transform", {"text": "WORLD", "operation": "lower"})
        assert result["success"] is True
        assert result["data"]["result"] == "world"

    def test_json_parse(self):
        registry = ToolRegistry()
        result = registry.execute("json_parse", {"json_string": '{"key": "value"}'})
        assert result["success"] is True
        assert result["data"]["parsed"] == {"key": "value"}

    def test_unknown_tool(self):
        registry = ToolRegistry()
        result = registry.execute("nonexistent", {})
        assert result["success"] is False
