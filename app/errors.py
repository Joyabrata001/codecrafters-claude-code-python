class ToolError(Exception):
    """Base class for tool related errors"""


class FileReadError(ToolError):
    pass


class FileWriteError(ToolError):
    pass


class BashExecutionError(ToolError):
    pass


class AgentLoopError(Exception):
    pass
