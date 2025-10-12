import asyncio
from typing import Literal

from langchain_core.messages import (
    BaseMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
    filter_messages,
)
from langgraph.graph import StateGraph
from langgraph.types import Command

from deepresearch.agents.research.graph import research_agent
from deepresearch.config.llm import LlmService
from deepresearch.core.constants import ConfigClass, GraphNode, OpikPrompts
from deepresearch.core.opik_prompts import Opik_prompts
from deepresearch.core.state import SupervisorState
from deepresearch.tools.tool import ConductResearch, ResearchComplete, think_tool
from deepresearch.tools.utils import get_today_str


from deepresearch.config.gemini_models import GeminiModel

def get_notes_from_tool_calls(messages: list[BaseMessage]) -> list[str]:
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
supervisor_model = LlmService.get_model()
supervisor_model_with_tools = supervisor_model.bind_tools(tools=supervisor_tool)

max_researcher_iteration = 6
max_concurrent_researcher = 3


async def supervisor(
    state: SupervisorState,
) -> Command[Literal[GraphNode.SUPERVISOR_TOOLS]]:
    supervisor_messages = state.get(ConfigClass.SUPERVISOR_MESSAGES, [])

    lead_researcher_prompt = Opik_prompts.get_prompt(
        prompt_name=OpikPrompts.LEAD_RESEARCHER_PROMPT
    )
    system_messages = lead_researcher_prompt.format(
        date=get_today_str(),
        max_concurrent_research_units=max_concurrent_researcher,
        max_researcher_iterations=max_researcher_iteration,
    )
    messages = [SystemMessage(content=system_messages)] + supervisor_messages
    response = await supervisor_model_with_tools.ainvoke(messages)

    return Command(
        goto=GraphNode.SUPERVISOR_TOOLS,
        update={
            ConfigClass.SUPERVISOR_MESSAGES: [response],
            ConfigClass.RESEARCH_ITERATIONS: state.get(
                ConfigClass.RESEARCH_ITERATIONS, 0
            )
            + 1,
        },
    )


async def supervisor_tools(
    state: SupervisorState,
) -> Command[Literal[GraphNode.SUPERVISOR, GraphNode.END]]:
    """Process tool calls from the supervisor LLM with optimized execution patterns.
    
    This function handles two types of tool calls differently based on their characteristics:
    
    1. **think_tool (Sequential Execution)**:
       - Processed using a simple for loop (synchronous, sequential)
       - Rationale: think_tool is a lightweight, instant operation that simply records
         reflections without any I/O operations or external API calls. It returns
         immediately with a confirmation message.
       - Impact: No performance benefit from parallelization; sequential processing
         keeps code simple and execution order predictable.
    
    2. **conduct_research (Concurrent Execution)**:
       - Processed using asyncio.gather() for parallel execution
       - Rationale: Each conduct_research call spawns an independent research_agent
         sub-graph that performs multiple web searches, LLM calls, and data processing.
         These are I/O-bound operations that can take several seconds to minutes.
       - Impact: Massive performance improvement - multiple research tasks execute
         simultaneously instead of waiting for each to complete sequentially.
         For example, 3 research tasks might complete in 30 seconds concurrently
         vs 90 seconds sequentially.
    
    This dual approach optimizes performance by:
    - Avoiding unnecessary overhead for lightweight operations (think_tool)
    - Maximizing throughput for expensive I/O-bound operations (conduct_research)
    
    Args:
        state: Current supervisor state containing messages and iteration count
        
    Returns:
        Command directing to either SUPERVISOR for next iteration or END to complete
    """
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
        tool_call["name"] == GraphNode.RESEARCH_COMPLETE
        for tool_call in most_recent_message.tool_calls
    )

    if exceed_iteration or no_tool_calls or research_complete:
        should_end = True
        next_step = GraphNode.END

    else:
        try:
            # Separate tool calls by type for optimized processing
            think_tools_call = [
                tool_call
                for tool_call in most_recent_message.tool_calls
                if tool_call["name"] == GraphNode.THINK_TOOL
            ]

            conduct_research_calls = [
                tool_call
                for tool_call in most_recent_message.tool_calls
                if tool_call["name"] == GraphNode.CONDUCT_RESEARCH
            ]

            # Process think_tool calls sequentially (for loop)
            # Why for loop? think_tool is a lightweight synchronous operation that
            # simply records a reflection string and returns instantly. No I/O,
            # no external calls, no benefit from parallelization. Sequential
            # execution is simpler and maintains predictable order.
            for tool_call in think_tools_call:
                observation = think_tool.invoke(tool_call["args"])
                tool_messages.append(
                    ToolMessage(
                        content=observation,
                        name=tool_call["name"],
                        tool_call_id=tool_call["id"],
                    )
                )

            # Process conduct_research calls concurrently (asyncio.gather)
            # Why asyncio.gather? Each conduct_research call invokes a full research
            # agent sub-graph that performs multiple web searches, LLM inference calls,
            # and content processing - operations that can take 10-60+ seconds each.
            # These are I/O-bound operations where threads/coroutines spend most time
            # waiting for external responses. Running them concurrently provides
            # massive performance gains (e.g., 3 tasks in 30s vs 90s sequentially).
            if conduct_research_calls:
                coros = [
                    research_agent.ainvoke(
                        {
                            ConfigClass.SUPERVISOR_MESSAGES: [
                                HumanMessage(
                                    content=tool_call["args"]["research_topic"]
                                )
                            ],
                            ConfigClass.RESEARCH_TOPIC: tool_call["args"][
                                "research_topic"
                            ],
                        }
                    )
                    for tool_call in conduct_research_calls
                ]
                tool_results = await asyncio.gather(*coros)

                research_tool_messages = [
                    ToolMessage(
                        content=result.get(
                            GraphNode.COMPRESSED_RESEARCH_GRAPH,
                            "Error synthesizing research report",
                        ),
                        name=tool_call["name"],
                        tool_call_id=tool_call["id"],
                    )
                    for result, tool_call in zip(tool_results, conduct_research_calls)
                ]

                tool_messages.extend(research_tool_messages)

                all_raw_notes = [
                    "\n".join(result.get("raw_notes", [])) for result in tool_results
                ]

        except Exception:
            should_end = True
            next_step = GraphNode.END

    if should_end:
        return Command(
            goto=next_step,
            update={
                ConfigClass.NOTES: get_notes_from_tool_calls(supervisor_messages),
                ConfigClass.RESEARCH_BRIEF: state.get(ConfigClass.RESEARCH_BRIEF, ""),
            },
        )
    else:
        return Command(
            goto=next_step,
            update={
                ConfigClass.SUPERVISOR_MESSAGES: tool_messages,
                ConfigClass.RAW_NOTES: all_raw_notes,
            },
        )


supervisor_builder = StateGraph(SupervisorState)

supervisor_builder.add_node(GraphNode.SUPERVISOR, supervisor)
supervisor_builder.add_node(GraphNode.SUPERVISOR_TOOLS, supervisor_tools)

supervisor_builder.add_edge(GraphNode.START, GraphNode.SUPERVISOR)
supervisor_agent = supervisor_builder.compile()
