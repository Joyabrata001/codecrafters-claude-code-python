"""Contains EnvConfig class definition"""

from dataclasses import dataclass


@dataclass(frozen=True)
class EnvConfig:
    """Defines dataclass to manage env state"""

    api_key: str | None
    base_url: str
    model: str
    max_agent_steps: int

    def validate(self):
        if not self.api_key:
            raise ValueError("Missing API key")
