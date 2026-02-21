"""Contains OpenRouterClient class definition"""

import json
from typing import Iterable, List

from openai import Omit, OpenAI
from openai.types.chat import ChatCompletionToolUnionParam
from app.env_config import EnvConfig
from app.file_tool_handler import FileToolHandler


class OpenRouterClient:
    """Manages LLM lifecycle and tools definitions"""

    def __init__(self, env_config: EnvConfig) -> None:
        if not env_config.api_key:
            raise ValueError("OPENROUTER_API_KEY is not set")

        self.client = OpenAI(api_key=env_config.api_key, base_url=env_config.base_url)
        self.model = env_config.model

    def get_tools_definition(self) -> Iterable[ChatCompletionToolUnionParam] | Omit:
        tools: List[ChatCompletionToolUnionParam] = [
            {
                "type": "function",
                "function": {
                    "name": "Read",
                    "description": "Read and return the contents of a file",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "file_path": {
                                "type": "string",
                                "description": "The path to the file to read",
                            }
                        },
                        "required": ["file_path"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "Write",
                    "description": "Write content to a file",
                    "parameters": {
                        "type": "object",
                        "required": ["file_path", "content"],
                        "properties": {
                            "file_path": {
                                "type": "string",
                                "description": "The path of the file to write to",
                            },
                            "content": {
                                "type": "string",
                                "description": "The content to write to the file",
                            },
                        },
                    },
                },
            },
        ]

        return tools

    def run_prompt(self, messages):
        try:
            return self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=self.get_tools_definition(),
            )
        except Exception as e:
            raise RuntimeError(f"An unexpected error occurred: {e}")

    def run_agent_loop(self, user_prompt: str):
        # Initialize message list
        messages = [{"role": "user", "content": user_prompt}]

        # Agent loop
        try:
            while True:
                # Get model response
                llm_response = self.run_prompt(messages=messages)
                message = llm_response.choices[0].message

                messages.append(message.model_dump())

                if not message.tool_calls:
                    return message.content

                tool_results = self.handle_tool_calls(message)
                messages.extend(tool_results)

        except RuntimeError as e:
            print(f"Stopping agent: {e}")
            return

    def handle_tool_calls(self, message):
        results = []

        if not message.tool_calls:
            return results

        for tool_call in message.tool_calls:
            if tool_call.type == "function":
                arguments = json.loads(tool_call.function.arguments)
                function_name = tool_call.function.name

                if function_name == "Read":
                    file_path = arguments.get("file_path")

                    content = FileToolHandler.read_file(file_path=file_path)

                    results.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "name": "Read",
                            "content": str(content),
                        }
                    )

                elif function_name == "Write":
                    file_path = arguments.get("file_path")
                    content = arguments.get("content")

                    status = FileToolHandler.write_file(
                        file_path=file_path,
                        content=content,
                    )

                    results.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "name": "Write",
                            "content": str(status),
                        }
                    )

        return results
