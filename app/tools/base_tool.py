"""Contains BaseTool class definition"""

from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseTool(ABC):
    """Interface for all the tools"""

    @abstractmethod
    def name(self) -> str:
        """Returns the tool name (useful for LLM)."""

    @abstractmethod
    def execute(self, arguments: Dict[str, Any]) -> str:
        """Execute tool with given arguments"""
