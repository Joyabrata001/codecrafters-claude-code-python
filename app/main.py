"""main.py"""

import argparse
import os

from app.env_config import EnvConfig
from app.errors import AgentLoopError
from app.open_router_client import OpenRouterClient

API_KEY = os.getenv("OPENROUTER_API_KEY")
BASE_URL = os.getenv("OPENROUTER_BASE_URL", default="https://openrouter.ai/api/v1")
DEFAULT_MODEL = "anthropic/claude-haiku-4.5"
MAX_AGENT_STEPS = 10


def main():
    p = argparse.ArgumentParser()
    p.add_argument("-p", required=True)
    args = p.parse_args()

    print(f"DEVDEV: {API_KEY}")

    env_config = EnvConfig(
        api_key=API_KEY,
        base_url=BASE_URL,
        model=DEFAULT_MODEL,
        max_agent_steps=MAX_AGENT_STEPS,
    )

    env_config.validate()

    try:
        # Initialize client
        app = OpenRouterClient(env_config=env_config)

        print(app.run_agent_loop(args.p))

    except AgentLoopError as e:
        print(f"Application error: {e}")


if __name__ == "__main__":
    main()
