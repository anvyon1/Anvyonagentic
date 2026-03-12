"""Tests for top-level imports and package structure"""

import pytest


class TestImports:
    def test_top_level_imports(self):
        from anvyonagentic import (
            Task, TaskDecomposer, LLMProvider, AnthropicProvider,
            AgentRegistry, WorkerAgent, BasicOrchestrator,
            ExecutorRouter, DelegationManager,
            ToolRegistry, Tool,
        )

    def test_version(self):
        import anvyonagentic
        assert anvyonagentic.__version__ == "3.0.0"

    def test_all_exports(self):
        import anvyonagentic
        assert len(anvyonagentic.__all__) == 11

    def test_core_submodule(self):
        from anvyonagentic.core import Task, TaskStatus, BasicOrchestrator, AgentRegistry

    def test_router_submodule(self):
        from anvyonagentic.router import ExecutorRouter, DelegationManager, DelegationContract

    def test_tools_submodule(self):
        from anvyonagentic.tools import ToolRegistry, Tool

    def test_enterprise_not_in_core(self):
        with pytest.raises(ImportError):
            from anvyonagentic.analyzer import PERTAnalyzer
        with pytest.raises(ImportError):
            from anvyonagentic.simulator import MonteCarloSimulator
        with pytest.raises(ImportError):
            from anvyonagentic.optimizer import RLOptimizer
        with pytest.raises(ImportError):
            from anvyonagentic.mcp import MCPClient
