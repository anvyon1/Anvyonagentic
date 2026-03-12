# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.1.0] - 2025-01-01

### Changed
- License changed from AGPL v3 / Commercial dual-license to **Apache License 2.0**
- Enterprise features (PERT analysis, Monte Carlo simulation, RL optimization, trust calibration, oversight/governance, delegation memory, human-in-the-loop) moved to separate **anvyonenterprise** package
- Removed `COMMERCIAL_LICENSE.md` (commercial features now in anvyonenterprise)
- Simplified package to focus on core multi-agent framework capabilities

## [2.0.0] - 2026-03-11

### Added
- Intelligent AI delegation system with full orchestration pipeline
- `Orchestrator` class coordinating the complete pipeline: PERT, Monte Carlo, RL, agent matching, delegation, execution, verification, trust update, memory storage
- `AgentRegistry` for managing worker agents with skills, trust scores, and cost
- `WorkerAgent` dataclass with 5 default agents: llm_reasoner, tool_executor, mcp_connector, code_agent, research_agent
- `TrustManager` for per-agent reputation tracking (success_rate x 0.5 + accuracy x 0.3 + reliability x 0.2)
- `DelegationManager` and `DelegationContract` for structured task delegation with authority levels (full, limited, supervised)
- `OversightAgent` for monitoring, verification, and failure recovery
- Recovery strategies: retry_same, delegate_to_better, escalate
- Human-in-the-loop support via approval callbacks for high-criticality tasks
- `DelegationMemory` for storing delegation history with JSON persistence
- Capability matching engine with scored agent selection (skill_match x 0.4 + trust x 0.3 + cost x 0.15 + success x 0.15)
- Extended `Task` with delegation attributes: complexity, criticality, cost, reversibility, uncertainty, verifiability, required_skills

### Changed
- Made `anthropic` an optional dependency (install with `pip install anvyonagentic[anthropic]`)
- Core library now has zero required dependencies (stdlib only)
- License changed from MIT to dual AGPL v3 / Commercial
- Updated version to 2.0.0

## [1.0.0] - 2026-01-23

### Added
- Initial release
- `Task` dataclass with PERT time estimates
- `TaskDecomposer` for LLM-powered task breakdown
- `PERTAnalyzer` for critical path analysis and duration estimation
- `MonteCarloSimulator` for probabilistic execution modeling
- `RLOptimizer` with Q-learning for speed/accuracy trade-off optimization
- `ExecutorRouter` for intelligent task routing (LLM, tools, MCP)
- `ToolRegistry` with built-in tools (calculate, datetime, text_transform, json_parse, web_search)
- `MCPClient` for Model Context Protocol integration
- `LLMProvider` abstract base and `AnthropicProvider` implementation
