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

"""Tests for Task data structure"""

import pytest
from anvyonagentic.core.task import Task, TaskStatus


class TestTask:
    def test_create_basic(self):
        task = Task(id="T1", description="Test task")
        assert task.id == "T1"
        assert task.description == "Test task"
        assert task.status == TaskStatus.PENDING

    def test_defaults(self):
        task = Task(id="T1", description="Test")
        assert task.execution_hint == "auto"
        assert task.depends_on == []
        assert task.base_accuracy == 0.95
        assert task.optimistic == 1.0
        assert task.most_likely == 2.0
        assert task.pessimistic == 4.0

    def test_expected_duration(self):
        task = Task(id="T1", description="Test",
                    optimistic=1.0, most_likely=2.0, pessimistic=6.0)
        expected = (1.0 + 4 * 2.0 + 6.0) / 6
        assert abs(task.expected_duration - expected) < 0.001

    def test_variance(self):
        task = Task(id="T1", description="Test",
                    optimistic=1.0, pessimistic=7.0)
        expected = ((7.0 - 1.0) / 6) ** 2
        assert abs(task.variance - expected) < 0.001

    def test_std_dev(self):
        task = Task(id="T1", description="Test",
                    optimistic=1.0, pessimistic=7.0)
        assert abs(task.std_dev - task.variance ** 0.5) < 0.001

    def test_to_dict(self):
        task = Task(id="T1", description="Test",
                    optimistic=1.0, most_likely=2.0, pessimistic=3.0,
                    base_accuracy=0.9)
        d = task.to_dict()
        assert d["id"] == "T1"
        assert d["description"] == "Test"
        assert d["optimistic"] == 1.0
        assert "expected_duration" in d
        assert "variance" in d

    def test_from_dict_camelcase(self):
        data = {
            "id": "T1",
            "description": "Test",
            "mostLikely": 3.0,
            "baseAccuracy": 0.85,
            "dependsOn": ["T0"],
            "executionHint": "llm",
        }
        task = Task.from_dict(data)
        assert task.most_likely == 3.0
        assert task.base_accuracy == 0.85
        assert task.depends_on == ["T0"]
        assert task.execution_hint == "llm"

    def test_from_dict_snakecase(self):
        data = {
            "id": "T1",
            "description": "Test",
            "most_likely": 3.0,
            "base_accuracy": 0.85,
            "depends_on": ["T0"],
            "execution_hint": "tool",
        }
        task = Task.from_dict(data)
        assert task.most_likely == 3.0
        assert task.base_accuracy == 0.85
        assert task.execution_hint == "tool"
