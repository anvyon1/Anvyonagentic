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

"""Tests for DelegationManager and DelegationContract"""

import pytest
from anvyonagentic.router.delegation import DelegationManager, DelegationContract


class TestDelegationManager:
    def test_create_contract(self):
        dm = DelegationManager()
        contract = dm.create_contract(
            task_id="T1",
            task_description="Test task",
            delegatee="llm_reasoner",
        )
        assert contract.id == "DC-1"
        assert contract.task_id == "T1"
        assert contract.delegatee == "llm_reasoner"
        assert contract.status == "pending"

    def test_complete_success(self):
        dm = DelegationManager()
        contract = dm.create_contract("T1", "Test", "agent1")
        dm.complete(contract.id, result={"output": "done"}, success=True, execution_time=1.5)
        c = dm.get(contract.id)
        assert c.status == "completed"
        assert c.success is True
        assert c.execution_time == 1.5

    def test_complete_failure(self):
        dm = DelegationManager()
        contract = dm.create_contract("T1", "Test", "agent1")
        dm.complete(contract.id, result=None, success=False, execution_time=0.5)
        c = dm.get(contract.id)
        assert c.status == "failed"
        assert c.success is False

    def test_get_all(self):
        dm = DelegationManager()
        dm.create_contract("T1", "Test 1", "agent1")
        dm.create_contract("T2", "Test 2", "agent2")
        assert len(dm.get_all()) == 2

    def test_get_stats(self):
        dm = DelegationManager()
        c1 = dm.create_contract("T1", "Test", "agent1")
        c2 = dm.create_contract("T2", "Test", "agent2")
        dm.complete(c1.id, None, True, 1.0)
        dm.complete(c2.id, None, False, 0.5)

        stats = dm.get_stats()
        assert stats["total"] == 2
        assert stats["completed"] == 1
        assert stats["failed"] == 1

    def test_to_dict(self):
        dm = DelegationManager()
        contract = dm.create_contract("T1", "Test", "agent1")
        d = contract.to_dict()
        assert d["id"] == contract.id
        assert d["task_id"] == "T1"
        assert d["delegatee"] == "agent1"

    def test_unique_ids(self):
        dm = DelegationManager()
        c1 = dm.create_contract("T1", "Test", "agent1")
        c2 = dm.create_contract("T2", "Test", "agent2")
        assert c1.id != c2.id
