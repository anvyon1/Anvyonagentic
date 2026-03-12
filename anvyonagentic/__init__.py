# Anvyon Agentic AI Framework
# Copyright (C) 2026 Anvyon
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed WITHOUT ANY WARRANTY.
# See the GNU Affero General Public License for more details.

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
