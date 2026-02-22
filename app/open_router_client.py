"""Contains OpenRouterClient class definition"""

import json
from typing import Iterable, List

from openai import Omit, OpenAI
from openai.types.chat import ChatCompletionToolUnionParam
from app.bash_tool_handler import BashToolHandler
from app.env_config import EnvConfig
from app.errors import AgentLoopError
from app.file_tool_handler import FileToolHandler
from app.tools_config import TOOLS_SPECIFICATIONS


class OpenRouterClient:
    """Manages LLM lifecycle and tools definitions"""

    def __init__(self, env_config: EnvConfig) -> None:
        self.client = OpenAI(api_key=env_config.api_key, base_url=env_config.base_url)
        self.model = env_config.model
        self.max_agent_steps = env_config.max_agent_steps

    def get_tools_definition(self) -> Iterable[ChatCompletionToolUnionParam] | Omit:
        tools: List[ChatCompletionToolUnionParam] = TOOLS_SPECIFICATIONS
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
            for _ in range(self.max_agent_steps):
                # Get model response
                llm_response = self.run_prompt(messages=messages)
                message = llm_response.choices[0].message

                messages.append(message.model_dump())

                if not message.tool_calls:
                    return message.content

                tool_results = self.handle_tool_calls(message)
                messages.extend(tool_results)

            raise AgentLoopError(f"Agent exceeded max steps ({self.max_agent_steps})")

        except RuntimeError as e:
            raise AgentLoopError(f"Stopping agent: {e}") from e

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

                elif function_name == "Bash":
                    command = arguments.get("command")

                    output = BashToolHandler.run_command(command=command)

                    results.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "name": "Write",
                            "content": output,
                        }
                    )

        return results
