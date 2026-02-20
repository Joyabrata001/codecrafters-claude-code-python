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

    # client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

    # chat = client.chat.completions.create(
    #     model="anthropic/claude-haiku-4.5",
    #     messages=[{"role": "user", "content": args.p}],
    #     tools=[
    #         {
    #             "type": "function",
    #             "function": {
    #                 "name": "Read",
    #                 "description": "Read and return the contents of a file",
    #                 "parameters": {
    #                     "type": "object",
    #                     "properties": {
    #                         "file_path": {
    #                             "type": "string",
    #                             "description": "The path to the file to read",
    #                         }
    #                     },
    #                     "required": ["file_path"],
    #                 },
    #             },
    #         }
    #     ],
    # )

    # if not chat.choices or len(chat.choices) == 0:
    #     raise RuntimeError("no choices in response")

    # choice = chat.choices[0]
    # msg = choice.message

    # if msg.tool_calls:
    #     tool_call = msg.tool_calls[0]

    #     if tool_call.type == "function":
    #         if tool_call.function.name == "Read":
    #             arguments = json.loads(tool_call.function.arguments)
    #             file_path = arguments.get("file_path")

    #             result = FileToolHandler.read_file(file_path=file_path)
    #             print(result)
    #         else:
    #             if msg.content:
    #                 print(msg.content)
    #     else:
    #         pass
    # else:
    #     pass
    try:
        app = OpenRouterClient(env_config=env_config)
        app.run_prompt(args.p)
    except (ValueError, KeyError, RuntimeError) as e:
        print(f"Application error: {e}")

if __name__ == "__main__":
    main()
