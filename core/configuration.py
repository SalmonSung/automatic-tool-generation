import os
from enum import Enum
from dataclasses import dataclass, fields
from typing import Any, Optional

from langchain_core.runnables import RunnableConfig



class PlannerProvider(Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    XAI = "xai"


class WriterProvider(Enum):
    ANTHROPIC = "anthropic"
    OPENAI = "openai"
    XAI = "xai"


class FilterProvider(Enum):
    OPENAI = "openai"

class FileType(Enum):
    CSV = "csv"
    JSON = "json"


class Index4File(Enum):
    TRUE = "true"
    FALSE = "false"


@dataclass(kw_only=True)
class Configuration:
    # planner_provider: PlannerProvider = PlannerProvider.ANTHROPIC
    # planner_model: str = "claude-3-7-sonnet-latest"
    planner_provider: PlannerProvider = PlannerProvider.OPENAI
    planner_model: str = "o3-mini"
    writer_provider: WriterProvider = WriterProvider.ANTHROPIC
    # writer_model: str = "claude-3-7-sonnet-latest"
    writer_model: str = "gpt-4.1-nano"
    filter_provider: FilterProvider = FilterProvider.OPENAI
    filter_model: str = "gpt-4.1-mini"
    file_type: FileType = FileType.CSV
    index4file: Index4File = Index4File.TRUE
    breadth: int = 5
    max_tokens: int = 32768

    @classmethod
    def from_runnable_config(
            cls, config: Optional[RunnableConfig] = None
    ) -> "Configuration":
        """Create a Configuration instance from a RunnableConfig."""
        configurable = (
            config["configurable"] if config and "configurable" in config else {}
        )
        values: dict[str, Any] = {
            f.name: os.environ.get(f.name.upper(), configurable.get(f.name))
            for f in fields(cls)
            if f.init
        }
        return cls(**{k: v for k, v in values.items() if v})