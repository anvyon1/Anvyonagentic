"""Tests for AgentRegistry and WorkerAgent"""

import pytest
from anvyonagentic.core.agent import AgentRegistry, WorkerAgent


class TestWorkerAgent:
    def test_create(self):
        agent = WorkerAgent(name="test", skills=["reasoning"])
        assert agent.name == "test"
        assert agent.skills == ["reasoning"]
        assert agent.trust_score == 0.8
        assert agent.total_tasks == 0


class TestAgentRegistry:
    def test_default_agents(self):
        registry = AgentRegistry()
        agents = registry.list()
        assert len(agents) == 4
        names = [a.name for a in agents]
        assert "llm_reasoner" in names
        assert "tool_executor" in names
        assert "code_agent" in names
        assert "research_agent" in names

    def test_get_agent(self):
        registry = AgentRegistry()
        agent = registry.get("llm_reasoner")
        assert agent is not None
        assert agent.name == "llm_reasoner"
        assert "reasoning" in agent.skills

    def test_get_nonexistent(self):
        registry = AgentRegistry()
        assert registry.get("nonexistent") is None

    def test_register_custom(self):
        registry = AgentRegistry()
        registry.register(WorkerAgent(
            name="custom_agent",
            skills=["sql", "database"],
            trust_score=0.9,
        ))
        agent = registry.get("custom_agent")
        assert agent is not None
        assert agent.trust_score == 0.9

    def test_unregister(self):
        registry = AgentRegistry()
        assert registry.unregister("llm_reasoner") is True
        assert registry.get("llm_reasoner") is None
        assert registry.unregister("nonexistent") is False

    def test_find_by_skill(self):
        registry = AgentRegistry()
        agents = registry.find_by_skill("reasoning")
        assert len(agents) >= 1
        assert any(a.name == "llm_reasoner" for a in agents)

    def test_update_stats(self):
        registry = AgentRegistry()
        agent = registry.get("llm_reasoner")
        initial_tasks = agent.total_tasks

        registry.update_stats("llm_reasoner", success=True)
        assert agent.total_tasks == initial_tasks + 1
        assert agent.successful_tasks == 1

        registry.update_stats("llm_reasoner", success=False)
        assert agent.total_tasks == initial_tasks + 2
        assert agent.successful_tasks == 1
        assert agent.success_rate == 0.5
