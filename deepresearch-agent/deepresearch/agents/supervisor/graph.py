
import asyncio
from typing import Literal

from langchain_core.messages import (
    BaseMessage,
    HumanMessage,
    AIMessage,
    SystemMessage,
    ToolMessage,
    filter_messages
)

from langgraph.graph import StateGraph
from langgraph.types import Command

from deepresearch.config.llm import LlmService
from deepresearch.core.opik_prompts import Opik_prompts
from deepresearch.core.constants import GraphNode, ConfigClass, OpikPrompts
from deepresearch.core.state import SupervisorState
from deepresearch.tools.tool import ConductResearch, ResearchComplete, think_tool
from deepresearch.tools.utils import get_today_str


def get_notes_from_tool_calls(messages: list[BaseMessage])->list[str]:
    """
    This function retrieves the compressed research findings that sub-agents
    return as ToolMessage content. When the supervisor delegates research to
    sub-agents via ConductResearch tool calls, each sub-agent returns its
    compressed findings as the content of a ToolMessage. This function
    extracts all such ToolMessage content to compile the final research notes.
    """

    return [
        tool_msg.content for tool_msg in filter_messages(messages, include_types="tool")
    ]