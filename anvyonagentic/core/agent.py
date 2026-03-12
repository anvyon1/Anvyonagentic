"""Agent Registry and Worker Agent system"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class WorkerAgent:
    """Represents a worker agent with skills"""
    name: str
    skills: List[str]
    trust_score: float = 0.8
    success_rate: float = 0.9
    cost: float = 0.5
    agent_type: str = "llm"
    description: str = ""
    total_tasks: int = 0
    successful_tasks: int = 0


class AgentRegistry:
    """Registry for managing worker agents"""

    def __init__(self):
        self._agents: Dict[str, WorkerAgent] = {}
        self._register_defaults()

    def _register_defaults(self):
        self.register(WorkerAgent(
            name="llm_reasoner",
            skills=["reasoning", "analysis", "text_generation", "summarization", "planning", "creative_writing"],
            trust_score=0.85, success_rate=0.9, cost=0.7, agent_type="llm",
            description="General-purpose reasoning and text generation agent"
        ))
        self.register(WorkerAgent(
            name="tool_executor",
            skills=["calculation", "data_processing", "json_parsing", "text_transform", "datetime"],
            trust_score=0.95, success_rate=0.95, cost=0.2, agent_type="tool",
            description="Executes structured operations using built-in tools"
        ))
        self.register(WorkerAgent(
            name="code_agent",
            skills=["coding", "debugging", "testing", "code_review", "refactoring"],
            trust_score=0.82, success_rate=0.88, cost=0.6, agent_type="llm",
            description="Specialized in code generation and analysis"
        ))
        self.register(WorkerAgent(
            name="research_agent",
            skills=["search", "research", "data_collection", "fact_checking", "comparison"],
            trust_score=0.78, success_rate=0.82, cost=0.4, agent_type="hybrid",
            description="Researches topics using search tools and LLM analysis"
        ))

    def register(self, agent: WorkerAgent) -> None:
        self._agents[agent.name] = agent

    def unregister(self, name: str) -> bool:
        if name in self._agents:
            del self._agents[name]
            return True
        return False

    def get(self, name: str) -> Optional[WorkerAgent]:
        return self._agents.get(name)

    def list(self) -> List[WorkerAgent]:
        return list(self._agents.values())

    def find_by_skill(self, skill: str) -> List[WorkerAgent]:
        return [a for a in self._agents.values()
                if any(skill.lower() in s.lower() or s.lower() in skill.lower() for s in a.skills)]

    def update_stats(self, name: str, success: bool) -> None:
        agent = self._agents.get(name)
        if not agent:
            return
        agent.total_tasks += 1
        if success:
            agent.successful_tasks += 1
        if agent.total_tasks > 0:
            agent.success_rate = agent.successful_tasks / agent.total_tasks
