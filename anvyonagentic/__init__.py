"""
Anvyon Agentic - Open-source multi-agent task framework

Core modules:
- core: Task structures, LLM provider, agents, basic orchestration
- router: Execution routing and basic delegation contracts
- tools: Tool registry and built-in tools

For advanced features (PERT analysis, Monte Carlo simulation, RL optimization,
trust calibration, oversight, governance, MCP), see anvyonenterprise.
"""

from anvyonagentic.core import (
    Task, TaskDecomposer, LLMProvider, AnthropicProvider,
    AgentRegistry, WorkerAgent, BasicOrchestrator,
)
from anvyonagentic.router import ExecutorRouter, DelegationManager
from anvyonagentic.tools import ToolRegistry, Tool

__version__ = "3.0.0"
__all__ = [
    "Task", "TaskDecomposer", "LLMProvider", "AnthropicProvider",
    "AgentRegistry", "WorkerAgent", "BasicOrchestrator",
    "ExecutorRouter", "DelegationManager",
    "ToolRegistry", "Tool",
]
