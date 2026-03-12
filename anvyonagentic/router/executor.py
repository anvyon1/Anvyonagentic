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

"""Execution Router - Routes tasks to optimal execution path"""

import json
import re
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from anvyonagentic.core.llm_provider import LLMProvider
from anvyonagentic.tools import ToolRegistry


@dataclass
class ExecutionDecision:
    """Decision about how to execute a task"""
    type: str
    reasoning: str
    tool_name: Optional[str] = None
    requires_llm: bool = False
    confidence: float = 0.5


@dataclass
class ExecutionResult:
    """Result of task execution"""
    type: str
    success: bool
    data: Any = None
    error: Optional[str] = None
    execution_time: float = 0.0
    steps: List[Dict] = field(default_factory=list)


class ExecutorRouter:
    """Routes tasks to optimal execution path (tool or LLM)"""

    def __init__(self, llm_provider: LLMProvider,
                 tool_registry: Optional[ToolRegistry] = None):
        self.llm = llm_provider
        self.tools = tool_registry or ToolRegistry()

    def analyze(self, task_description: str) -> ExecutionDecision:
        tool_descriptions = self.tools.get_descriptions()
        tool_names = [t.name for t in self.tools.list()]

        prompt = f"""You are an AI execution router. Analyze this task and decide the best execution path.

TASK: "{task_description}"

AVAILABLE TOOLS:
{tool_descriptions or 'None registered'}

IMPORTANT RULES:
- Only choose "tool" if the toolName exactly matches one of the available tools
- If no tools match, choose "llm"
- Default to "llm" for reasoning, analysis, creative, or general tasks

Return ONLY a JSON object:
{{
  "type": "tool|llm",
  "reasoning": "Brief explanation",
  "toolName": "exact_tool_name or null",
  "requiresLLM": true/false,
  "confidence": 0.0-1.0
}}"""

        try:
            response = self.llm.call(prompt)
            json_match = re.search(r'\{[\s\S]*\}', response.text)

            if json_match:
                data = json.loads(json_match.group())
                decision = ExecutionDecision(
                    type=data.get("type", "llm"),
                    reasoning=data.get("reasoning", ""),
                    tool_name=data.get("toolName"),
                    requires_llm=data.get("requiresLLM", False),
                    confidence=data.get("confidence", 0.5)
                )
                return self._validate_decision(decision, tool_names)
        except Exception:
            pass

        return ExecutionDecision(
            type="llm",
            reasoning="Defaulting to LLM for general task processing",
            requires_llm=True,
            confidence=0.5
        )

    def _validate_decision(self, decision: ExecutionDecision,
                           tool_names: List[str]) -> ExecutionDecision:
        if decision.type == "tool":
            if not decision.tool_name or decision.tool_name not in tool_names:
                return ExecutionDecision(
                    type="llm",
                    reasoning=f"Tool '{decision.tool_name}' not found. Falling back to LLM.",
                    requires_llm=True,
                    confidence=0.6
                )
        return decision

    def execute(self, task_description: str) -> ExecutionResult:
        import time
        start_time = time.time()
        steps = []

        decision = self.analyze(task_description)
        steps.append({"action": "analyze", "decision": decision.type,
                       "reasoning": decision.reasoning})

        try:
            if decision.type == "tool" and decision.tool_name:
                result = self.tools.execute(decision.tool_name,
                                            {"input": task_description})
                steps.append({"action": "tool_execute", "tool": decision.tool_name,
                               "result": result})
                return ExecutionResult(
                    type="tool",
                    success=result.get("success", False),
                    data=result.get("data"),
                    error=result.get("error"),
                    execution_time=time.time() - start_time,
                    steps=steps
                )
            else:
                response = self.llm.call(
                    f"Complete this task:\n\n{task_description}")
                steps.append({"action": "llm_call",
                               "response_length": len(response.text)})
                return ExecutionResult(
                    type="llm",
                    success=True,
                    data={"response": response.text},
                    execution_time=time.time() - start_time,
                    steps=steps
                )
        except Exception as e:
            return ExecutionResult(
                type=decision.type,
                success=False,
                error=str(e),
                execution_time=time.time() - start_time,
                steps=steps
            )
