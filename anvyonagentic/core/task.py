"""Task data structures"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Dict, Any


class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Task:
    """Represents a task with basic time estimates and execution metadata"""

    id: str
    description: str
    optimistic: float = 1.0
    most_likely: float = 2.0
    pessimistic: float = 4.0
    base_accuracy: float = 0.95
    depends_on: List[str] = field(default_factory=list)
    execution_hint: str = "auto"
    status: TaskStatus = TaskStatus.PENDING
    result: Optional[Any] = None
    error: Optional[str] = None
    execution_time: float = 0.0

    @property
    def expected_duration(self) -> float:
        return (self.optimistic + 4 * self.most_likely + self.pessimistic) / 6

    @property
    def variance(self) -> float:
        return ((self.pessimistic - self.optimistic) / 6) ** 2

    @property
    def std_dev(self) -> float:
        return self.variance ** 0.5

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "description": self.description,
            "optimistic": self.optimistic,
            "most_likely": self.most_likely,
            "pessimistic": self.pessimistic,
            "base_accuracy": self.base_accuracy,
            "depends_on": self.depends_on,
            "execution_hint": self.execution_hint,
            "status": self.status.value,
            "expected_duration": self.expected_duration,
            "variance": self.variance,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Task":
        return cls(
            id=data["id"],
            description=data["description"],
            optimistic=data.get("optimistic", 1.0),
            most_likely=data.get("mostLikely", data.get("most_likely", 2.0)),
            pessimistic=data.get("pessimistic", 4.0),
            base_accuracy=data.get("baseAccuracy", data.get("base_accuracy", 0.95)),
            depends_on=data.get("dependsOn", data.get("depends_on", [])),
            execution_hint=data.get("executionHint", data.get("execution_hint", "auto")),
        )
