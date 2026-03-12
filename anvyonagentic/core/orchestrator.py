"""BasicOrchestrator - Simple delegation pipeline for open-source use"""

import time
from typing import List, Dict, Any, Optional
from anvyonagentic.core.task import Task
from anvyonagentic.core.agent import AgentRegistry, WorkerAgent
from anvyonagentic.router.delegation import DelegationManager, DelegationContract
from anvyonagentic.router.executor import ExecutorRouter
from anvyonagentic.tools import ToolRegistry


class BasicOrchestrator:
    """Simple orchestrator: decompose -> match agents -> delegate -> execute

    For the full 10-step pipeline with PERT analysis, Monte Carlo simulation,
    RL optimization, trust calibration, oversight, and governance,
    use anvyonenterprise.Orchestrator.
    """

    def __init__(self, llm_provider=None, tool_registry: ToolRegistry = None):
        self.llm = llm_provider
        self.tools = tool_registry or ToolRegistry()
        self.agent_registry = AgentRegistry()
        self.delegation_manager = DelegationManager()

        if llm_provider:
            self.router = ExecutorRouter(llm_provider, self.tools)
        else:
            self.router = None

    def run(self, tasks: List[Task]) -> Dict[str, Any]:
        """Run the basic pipeline on tasks"""

        assignments = self._match_agents(tasks)
        contracts = self._create_contracts(tasks, assignments)
        summaries = self._execute_all(tasks, assignments, contracts)

        return {
            "delegations": summaries,
            "delegation_stats": self.delegation_manager.get_stats()
        }

    def _match_agents(self, tasks: List[Task]) -> List[WorkerAgent]:
        agents = []
        for task in tasks:
            skills = self._infer_skills(task)
            matches = self.agent_registry.find_by_skill(skills[0]) if skills else []
            agent = matches[0] if matches else self.agent_registry.get("llm_reasoner")
            agents.append(agent)
        return agents

    def _infer_skills(self, task: Task) -> List[str]:
        hint = task.execution_hint
        if hint == "tool":
            return ["calculation", "data_processing"]
        elif hint == "llm":
            return ["reasoning", "analysis"]
        return ["reasoning"]

    def _create_contracts(self, tasks: List[Task],
                          agents: List[WorkerAgent]) -> List[DelegationContract]:
        contracts = []
        for task, agent in zip(tasks, agents):
            contract = self.delegation_manager.create_contract(
                task_id=task.id,
                task_description=task.description,
                delegatee=agent.name
            )
            contracts.append(contract)
        return contracts

    def _execute_all(self, tasks: List[Task], agents: List[WorkerAgent],
                     contracts: List[DelegationContract]) -> List[Dict[str, Any]]:
        summaries = []

        for task, agent, contract in zip(tasks, agents, contracts):
            start_time = time.time()
            try:
                if self.router:
                    exec_result = self.router.execute(task.description)
                    if hasattr(exec_result, 'success'):
                        success = exec_result.success
                        result_data = {"success": success,
                                       "data": getattr(exec_result, 'data', None),
                                       "error": getattr(exec_result, 'error', None)}
                    else:
                        success = True
                        result_data = {"success": True, "data": exec_result}
                else:
                    success = True
                    result_data = {"success": True, "data": None,
                                   "note": "No LLM provider - simulated execution"}
                exec_time = time.time() - start_time
            except Exception as e:
                success = False
                result_data = {"success": False, "error": str(e)}
                exec_time = time.time() - start_time

            self.delegation_manager.complete(contract.id, result_data, success, exec_time)
            self.agent_registry.update_stats(agent.name, success)

            summaries.append({
                "task_id": task.id,
                "agent": agent.name,
                "contract_id": contract.id,
                "success": success,
                "execution_time": exec_time,
            })

        return summaries
