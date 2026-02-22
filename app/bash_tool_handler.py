"""Contains BashHandler class definition"""

import shlex
import subprocess

from app.errors import BashExecutionError


class BashToolHandler:
    """Handles the execution of shell command"""

    @staticmethod
    def run_command(command: str) -> str:
        """Run shell command"""
        try:
            args = shlex.split(command)
            result = subprocess.run(
                args=args,
                capture_output=True,
                text=True,
                encoding="utf-8",
                check=True,
                timeout=10,
            )

            return result.stdout or ""

        except subprocess.TimeoutExpired as e:
            raise BashExecutionError(f"Command '{command}' timed out after 10s") from e
        except subprocess.CalledProcessError as e:
            raise BashExecutionError(f"Command failed: {e.stderr.strip()}") from e
        except FileNotFoundError as e:
            raise BashExecutionError(f"Executable not found for: {command}") from e
        except Exception as e:
            raise BashExecutionError(f"Unexpected shell error: {e}") from e
