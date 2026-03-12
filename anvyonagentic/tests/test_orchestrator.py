"""Tests for BasicOrchestrator (no LLM required)"""

import pytest
from anvyonagentic.core.task import Task
from anvyonagentic.core.orchestrator import BasicOrchestrator


def _make_tasks():
    return [
        Task(id="T1", description="Analyze input data",
             optimistic=0.5, most_likely=1.0, pessimistic=2.0,
             base_accuracy=0.95, execution_hint="llm"),
        Task(id="T2", description="Process records",
             optimistic=0.3, most_likely=0.8, pessimistic=1.5,
             base_accuracy=0.98, depends_on=["T1"], execution_hint="tool"),
        Task(id="T3", description="Generate report",
             optimistic=0.5, most_likely=1.0, pessimistic=2.0,
             base_accuracy=0.92, depends_on=["T2"], execution_hint="llm"),
    ]


class TestBasicOrchestrator:
    def test_run_without_llm(self):
        orchestrator = BasicOrchestrator()
        results = orchestrator.run(_make_tasks())
        assert "delegations" in results
        assert "delegation_stats" in results

    def test_delegation_count(self):
        orchestrator = BasicOrchestrator()
        results = orchestrator.run(_make_tasks())
        assert len(results["delegations"]) == 3

    def test_all_tasks_get_agents(self):
        orchestrator = BasicOrchestrator()
        results = orchestrator.run(_make_tasks())
        for d in results["delegations"]:
            assert "agent" in d
            assert d["agent"] is not None

    def test_all_tasks_succeed_without_llm(self):
        orchestrator = BasicOrchestrator()
        results = orchestrator.run(_make_tasks())
        for d in results["delegations"]:
            assert d["success"] is True

    def test_delegation_stats(self):
        orchestrator = BasicOrchestrator()
        results = orchestrator.run(_make_tasks())
        stats = results["delegation_stats"]
        assert stats["total"] == 3
        assert stats["completed"] == 3

    def test_single_task(self):
        orchestrator = BasicOrchestrator()
        tasks = [Task(id="T1", description="Simple task")]
        results = orchestrator.run(tasks)
        assert len(results["delegations"]) == 1
        assert results["delegations"][0]["success"] is True

    def test_empty_tasks(self):
        orchestrator = BasicOrchestrator()
        results = orchestrator.run([])
        assert len(results["delegations"]) == 0
