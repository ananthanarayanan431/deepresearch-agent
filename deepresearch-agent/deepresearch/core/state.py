import operator
from typing import Annotated, Optional, Sequence

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
