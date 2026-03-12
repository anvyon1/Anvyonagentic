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

"""Basic Delegation Contract System"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import time


@dataclass
class DelegationContract:
    id: str
    task_id: str
    task_description: str
    delegator: str = "orchestrator"
    delegatee: str = ""
    allowed_tools: List[str] = field(default_factory=list)
    constraints: List[str] = field(default_factory=list)
    expected_output: str = ""
    timestamp: float = 0.0
    status: str = "pending"
    result: Any = None
    success: Optional[bool] = None
    execution_time: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "task_id": self.task_id,
            "task_description": self.task_description,
            "delegator": self.delegator,
            "delegatee": self.delegatee,
            "status": self.status,
            "success": self.success,
            "execution_time": self.execution_time,
            "timestamp": self.timestamp
        }


class DelegationManager:
    """Manages basic delegation contracts"""

    def __init__(self):
        self._contracts: Dict[str, DelegationContract] = {}
        self._counter = 0

    def create_contract(self, task_id: str, task_description: str,
                        delegatee: str) -> DelegationContract:
        self._counter += 1
        contract_id = f"DC-{self._counter}"

        contract = DelegationContract(
            id=contract_id,
            task_id=task_id,
            task_description=task_description,
            delegatee=delegatee,
            timestamp=time.time()
        )
        self._contracts[contract_id] = contract
        return contract

    def complete(self, contract_id: str, result: Any, success: bool,
                 execution_time: float) -> None:
        c = self._contracts.get(contract_id)
        if c:
            c.status = "completed" if success else "failed"
            c.result = result
            c.success = success
            c.execution_time = execution_time

    def get(self, contract_id: str) -> Optional[DelegationContract]:
        return self._contracts.get(contract_id)

    def get_all(self) -> List[DelegationContract]:
        return list(self._contracts.values())

    def get_stats(self) -> Dict[str, int]:
        all_c = self.get_all()
        return {
            "total": len(all_c),
            "completed": sum(1 for c in all_c if c.status == "completed"),
            "failed": sum(1 for c in all_c if c.status == "failed"),
            "active": sum(1 for c in all_c if c.status == "active")
        }
