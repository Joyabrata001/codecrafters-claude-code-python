"""Contains EnvConfig class definition"""

from dataclasses import dataclass


@dataclass
class EnvConfig:
    """Defines dataclass to manage env state"""

    api_key: str | None
    base_url: str
    model: str
