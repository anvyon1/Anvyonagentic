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

"""Task decomposition using LLM"""

import json
import re
from typing import List, Optional
from anvyonagentic.core.task import Task
from anvyonagentic.core.llm_provider import LLMProvider


class TaskDecomposer:
    """Decomposes complex tasks into subtasks using LLM"""
    
    def __init__(self, llm_provider: LLMProvider):
        self.llm = llm_provider
    
    def decompose(self, task_description: str, max_subtasks: int = 10) -> List[Task]:
        """Decompose a task description into subtasks with PERT estimates"""
        
        prompt = f"""You are a task decomposition expert. Break down this task into subtasks.

TASK: "{task_description}"

For each subtask provide:
- id: Unique identifier (T1, T2, etc.)
- description: Clear description of what needs to be done
- optimistic: Best-case time estimate (hours)
- mostLikely: Most likely time estimate (hours)
- pessimistic: Worst-case time estimate (hours)
- baseAccuracy: Expected accuracy/success rate (0.0-1.0)
- dependsOn: List of task IDs this depends on
- executionHint: One of "llm", "tool", "mcp", or "auto"

Return ONLY a JSON array of tasks:
[
  {{
    "id": "T1",
    "description": "...",
    "optimistic": 1,
    "mostLikely": 2,
    "pessimistic": 4,
    "baseAccuracy": 0.95,
    "dependsOn": [],
    "executionHint": "llm"
  }}
]

Keep subtasks to {max_subtasks} or fewer. Focus on actionable steps."""

        response = self.llm.call(prompt)
        
        json_match = re.search(r'\[[\s\S]*\]', response.text)
        if not json_match:
            return [Task(id="T1", description=task_description)]
        
        try:
            tasks_data = json.loads(json_match.group())
            return [Task.from_dict(t) for t in tasks_data]
        except json.JSONDecodeError:
            return [Task(id="T1", description=task_description)]
