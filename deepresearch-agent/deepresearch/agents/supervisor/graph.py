
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

from deepresearch.agents.research.graph import research_agent


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

supervisor_tool = [think_tool, ConductResearch, ResearchComplete]
supervisor_model = LlmService.get_model(model_name="gpt-4.1")
supervisor_model_with_tools = supervisor_model.bind_tools(tools=supervisor_tool)

max_researcher_iteration = 6
max_concurrent_researcher = 3

async def supervisor(state: SupervisorState) -> Command[Literal[GraphNode.SUPERVISOR_TOOLS]]:

    supervisor_messages = state.get(ConfigClass.SUPERVISOR_MESSAGES, [])

    lead_researcher_prompt = Opik_prompts.get_prompt(prompt_name=OpikPrompts.LEAD_RESEARCHER_PROMPT)
    system_messages = lead_researcher_prompt.format(
        date=get_today_str(),
        max_concurrent_research_units=max_concurrent_researcher,
        max_researcher_iterations=max_researcher_iteration
    )
    messages = [SystemMessage(content=system_messages)] + supervisor_messages
    response = await supervisor_model_with_tools.ainvoke(messages)

    return Command(
        goto=GraphNode.SUPERVISOR_TOOLS,
        update={
            ConfigClass.SUPERVISOR_MESSAGES: [response],
            ConfigClass.RESEARCH_ITERATIONS: state.get(ConfigClass.RESEARCH_ITERATIONS, 0) + 1 
        }
    )

async def supervisor_tools(state: SupervisorState)-> Command[Literal[GraphNode.SUPERVISOR, GraphNode.END]]:
    
    supervisor_messages = state.get(ConfigClass.SUPERVISOR_MESSAGES, [])
    research_iteration = state.get(ConfigClass.RESEARCH_ITERATIONS, 0)
    most_recent_message = supervisor_messages[-1]

    tool_messages = []
    all_raw_notes = []
    next_step = GraphNode.SUPERVISOR
    should_end = False

    exceed_iteration = research_iteration >= max_researcher_iteration
    no_tool_calls = not most_recent_message.tool_calls
    research_complete = any(
        tool_call['name']==GraphNode.RESEARCH_COMPLETE
        for tool_call in most_recent_message.tool_calls
    )

    if exceed_iteration or no_tool_calls or research_complete:
        should_end = True
        next_step = GraphNode.END
    
    else:
        try:
            think_tools_call = [
                tool_call for tool_call in most_recent_message.tool_calls
                if tool_call['name'] == GraphNode.THINK_TOOL
            ]

            conduct_research_calls = [
                tool_call for tool_call in most_recent_message.tool_calls
                if tool_call['name'] == GraphNode.CONDUCT_RESEARCH
            ]

            for tool_call in think_tools_call:
                observation = think_tool.invoke(tool_call['args'])
                tool_messages.append(
                    ToolMessage(
                        content=observation,
                        name=tool_call["name"],
                        tool_call_id=tool_call["id"]
                    )
                )
            
            if conduct_research_calls:
                coros = [
                    research_agent.ainvoke({
                        ConfigClass.SUPERVISOR_MESSAGES : [HumanMessage(content=tool_call["args"]["research_topic"])],
                        ConfigClass.RESEARCH_TOPIC: tool_call["args"]["research_topic"]
                    }) 
                    for tool_call in conduct_research_calls
                ]
                tool_results = await asyncio.gather(*coros)

                research_tool_messages = [
                    ToolMessage(
                        content=result.get(GraphNode.COMPRESSED_RESEARCH_GRAPH, "Error synthesizing research report"),
                        name = tool_call['name'],
                        tool_call_id = tool_call['id']
                    ) for result, tool_call in zip(tool_results, conduct_research_calls)
                ]

                tool_messages.extend(research_tool_messages)

                all_raw_notes = [
                    "\n".join(result.get("raw_notes", [])) 
                    for result in tool_results
                ]
            
        except Exception as e:
            should_end = True
            next_step = GraphNode.END

        
    if should_end:
        return Command(
            goto=next_step,
            update={
                ConfigClass.NOTES: get_notes_from_tool_calls(supervisor_messages),
                ConfigClass.RESEARCH_BRIEF: state.get(ConfigClass.RESEARCH_BRIEF, "")
            }
        )
    else:
        return Command(
            goto=next_step,
            update={
                ConfigClass.SUPERVISOR_MESSAGES: tool_messages,
                ConfigClass.RAW_NOTES: all_raw_notes
            }
        )


supervisor_builder = StateGraph(SupervisorState)

supervisor_builder.add_node(GraphNode.SUPERVISOR, supervisor)
supervisor_builder.add_node(GraphNode.SUPERVISOR_TOOLS, supervisor_tools)

supervisor_builder.add_edge(GraphNode.START, GraphNode.SUPERVISOR)
supervisor_agent = supervisor_builder.compile()