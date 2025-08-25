import operator
from typing import Annotated, List, Optional, Sequence

from langchain_core.messages import BaseMessage
from langgraph.graph import MessagesState, add_messages


class AgentInputState(MessagesState):
    pass


class AgentState(MessagesState):
    research_brief: Optional[str]
    supervisor_messages: Annotated[Sequence[BaseMessage], add_messages]
    raw_notes: Annotated[list[str], operator.add]
    notes: Annotated[list[str], operator.add]
    final_report: str


class ResearcherState(MessagesState):
    researcher_messages: Annotated[Sequence[BaseMessage], add_messages]
    tool_call_iterations: int
    research_topic: str
    compressed_research: str
    raw_notes: Annotated[List[str], operator.add]


class ResearcherOutputState(MessagesState):
    compressed_research: str
    raw_notes: Annotated[List[str], operator.add]
    researcher_messages: Annotated[Sequence[BaseMessage], add_messages]
