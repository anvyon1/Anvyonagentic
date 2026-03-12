# Anvyon Agentic

**Open-source multi-agent framework for task decomposition, delegation, and execution.**

Anvyon Agentic is a Python library for building multi-agent systems that decompose, delegate, and execute complex tasks. It provides a simple yet powerful foundation for agentic workflows with pluggable LLM providers.

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

## Features

- **Zero required dependencies** — core library uses only Python stdlib
- **Task decomposition** — break complex tasks into manageable subtasks via LLM
- **Agent registry** — register, list, and find agents by skill
- **Basic delegation** — create and manage delegation contracts
- **Executor routing** — route tasks to the right execution path (LLM or tool)
- **Built-in tools** — calculate, datetime, text_transform, json_parse, web_search
- **Pluggable LLM providers** — bring your own LLM or use the built-in Anthropic provider

> **Looking for advanced features?** PERT analysis, Monte Carlo simulation, RL optimization, trust calibration, oversight/governance, delegation memory, and human-in-the-loop are available in the **[anvyonenterprise](https://github.com/anvyon/anvyonenterprise)** package.

## Installation

```bash
pip install anvyonagentic
```

With Anthropic (Claude) support:

```bash
pip install anvyonagentic[anthropic]
```

For development:

```bash
pip install anvyonagentic[dev]
```

## Quick Start

```python
from anvyonagentic import Task, AgentRegistry, BasicOrchestrator, ToolRegistry

tasks = [
    Task(id="T1", description="Parse user input",
         optimistic=0.5, most_likely=1.0, pessimistic=2.0),
    Task(id="T2", description="Process data",
         optimistic=1.0, most_likely=2.0, pessimistic=3.0,
         depends_on=["T1"]),
]

registry = AgentRegistry()
agents = registry.find_by_skill("reasoning")
print(f"Found agent: {agents[0].name}")

orchestrator = BasicOrchestrator()
results = orchestrator.run(tasks)
print(results)

tools = ToolRegistry()
result = tools.execute("calculate", {"expression": "2 + 2 * 3"})
print(result)
```

## Architecture

### Modules

| Module | Description |
|---|---|
| `anvyonagentic.core` | Task, AgentRegistry, BasicOrchestrator |
| `anvyonagentic.router` | ExecutorRouter, DelegationManager |
| `anvyonagentic.tools` | ToolRegistry with built-in tools |

### Default Agents

| Agent | Type | Skills |
|---|---|---|
| `llm_reasoner` | llm | reasoning, analysis, text generation, planning |
| `tool_executor` | tool | calculation, data processing, JSON parsing |
| `code_agent` | llm | coding, debugging, testing, code review |
| `research_agent` | hybrid | search, research, fact-checking |

## Advanced Usage

### Custom Agents

```python
from anvyonagentic import AgentRegistry, WorkerAgent

registry = AgentRegistry()

registry.register(WorkerAgent(
    name="sql_expert",
    skills=["sql", "database", "query_optimization"],
    agent_type="tool",
    description="Specialized SQL and database agent"
))

agents = registry.find_by_skill("database")
print(f"Found agent: {agents[0].name}")
```

### Built-in Tools

```python
from anvyonagentic import ToolRegistry

tools = ToolRegistry()

result = tools.execute("calculate", {"expression": "2 + 2 * 3"})
print(result)  # {"success": True, "data": {"result": 8}}

result = tools.execute("datetime", {"format": "iso"})
result = tools.execute("text_transform", {"text": "hello", "operation": "upper"})
```

## Enterprise Features

For advanced capabilities including PERT analysis, Monte Carlo simulation, RL optimization, trust calibration, oversight/governance, delegation memory, and human-in-the-loop approval, see the **[anvyonenterprise](https://github.com/anvyon/anvyonenterprise)** package.



## Contributing

Contributions are welcome. Please open an issue first to discuss what you would like to change.

```bash
git clone https://github.com/anvyon/anvyonagentic.git
cd anvyonagentic
pip install -e ".[dev]"
pytest
```

## License

This project is licensed under the **GNU Affero General Public License v3.0** (AGPL-3.0). See [LICENSE](LICENSE) for the full text.
