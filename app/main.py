import argparse
import json
import os
import sys

from openai import OpenAI

from app.env_config import EnvConfig
from app.file_tool_handler import FileToolHandler
from app.open_router_client import OpenRouterClient

API_KEY = os.getenv("OPENROUTER_API_KEY")
BASE_URL = os.getenv("OPENROUTER_BASE_URL", default="https://openrouter.ai/api/v1")
DEFAULT_MODEL = "anthropic/claude-haiku-4.5"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("-p", required=True)
    args = p.parse_args()

    env_config = EnvConfig(
        api_key=API_KEY,
        base_url=BASE_URL,
        model=DEFAULT_MODEL,
    )

    try:
        app = OpenRouterClient(env_config=env_config)

        chat = app.run_prompt(args.p)

        if isinstance(chat, str):
            print(f"run_prompt error: {chat}")
            return

        if not chat or not chat.choices:
            print("No response received from the model")
            return

        print(chat.choices[0].message.content)

    except (ValueError, KeyError, RuntimeError) as e:
        print(f"Application error: {e}")


if __name__ == "__main__":
    main()
