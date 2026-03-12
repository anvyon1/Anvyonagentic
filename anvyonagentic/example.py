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

#!/usr/bin/env python3
"""
Example usage of Anvyon Agentic (open-source core)

Demonstrates: Task creation, agent registry, basic delegation, and
the BasicOrchestrator pipeline.

For advanced features (PERT, Monte Carlo, RL, trust, oversight, governance),
see anvyonenterprise.
"""

from anvyonagentic.core.task import Task
from anvyonagentic.core.agent import AgentRegistry
from anvyonagentic.core.orchestrator import BasicOrchestrator
from anvyonagentic.router.delegation import DelegationManager
from anvyonagentic.tools import ToolRegistry


def main():
    print("=" * 60)
    print("Anvyon Agentic - Open Source Core Demo")
    print("=" * 60)

    tasks = [
        Task(id="T1", description="Parse customer support query",
             optimistic=0.5, most_likely=1.0, pessimistic=2.0,
             base_accuracy=0.95, execution_hint="llm"),
        Task(id="T2", description="Look up order in database",
             optimistic=0.3, most_likely=0.8, pessimistic=1.5,
             base_accuracy=0.98, depends_on=["T1"], execution_hint="tool"),
        Task(id="T3", description="Generate response to customer",
             optimistic=0.5, most_likely=1.0, pessimistic=2.0,
             base_accuracy=0.92, depends_on=["T2"], execution_hint="llm"),
    ]

    print("\n[1] Tasks")
    print("-" * 40)
    for t in tasks:
        print(f"  {t.id}: {t.description} (expected: {t.expected_duration:.2f}h)")

    print("\n[2] Agent Registry")
    print("-" * 40)
    registry = AgentRegistry()
    for agent in registry.list():
        print(f"  {agent.name} ({agent.agent_type}): "
              f"{', '.join(agent.skills[:3])}...")

    print("\n[3] Agent Matching (by skill)")
    print("-" * 40)
    for task in tasks:
        skill = "reasoning" if task.execution_hint == "llm" else "calculation"
        matches = registry.find_by_skill(skill)
        agent_name = matches[0].name if matches else "none"
        print(f"  {task.id} -> {agent_name}")

    print("\n[4] Basic Delegation")
    print("-" * 40)
    dm = DelegationManager()
    for task in tasks:
        contract = dm.create_contract(
            task_id=task.id,
            task_description=task.description,
            delegatee="llm_reasoner"
        )
        print(f"  {contract.id}: {task.id} -> {contract.delegatee}")

    print("\n[5] Built-in Tools")
    print("-" * 40)
    tools = ToolRegistry()
    result = tools.execute("calculate", {"expression": "2 + 2 * 3"})
    print(f"  calculate('2 + 2 * 3') = {result}")
    result = tools.execute("text_transform", {"text": "hello", "operation": "upper"})
    print(f"  text_transform('hello', 'upper') = {result}")

    print("\n[6] BasicOrchestrator Pipeline")
    print("-" * 40)
    orchestrator = BasicOrchestrator()
    results = orchestrator.run(tasks)

    print(f"  Delegations: {len(results['delegations'])}")
    for d in results['delegations']:
        status = "OK" if d['success'] else "FAIL"
        print(f"    {d['task_id']} -> {d['agent']} [{status}]")

    print(f"\n  Stats: {results['delegation_stats']}")

    print("\n" + "=" * 60)
    print("For PERT analysis, Monte Carlo simulation, RL optimization,")
    print("trust calibration, oversight, and governance, upgrade to:")
    print("  pip install anvyonenterprise")
    print("=" * 60)


if __name__ == "__main__":
    main()
