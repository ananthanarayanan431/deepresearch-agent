
from typing import Literal
from langgraph.graph import StateGraph
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage, filter_messages

from deepresearch.agents.research.summarizer import summarization_model
from deepresearch.config.llm import LlmService
from deepresearch.core.state import ResearcherOutputState, ResearcherState
from deepresearch.tools.tool import tavily_search, think_tool
from deepresearch.tools.utils import get_today_str
from deepresearch.core.opik_prompts import Opik_prompts
from deepresearch.core.constants import GraphNode, ConfigClass, OpikPrompts

tools = [tavily_search, think_tool]
tools_by_name = {tool.name: tool for tool in tools}

model = LlmService.get_model(model_name="gpt-4.1")
model_with_tools = model.bind_tools(tools)

summarization_model = LlmService.get_model(model_name="gpt-4o-mini")
compress_model = LlmService.get_model(model_name="gpt-4.1")

def llm_call(state: ResearcherState):
    """Analyze the current state and determine the next step"""

    research_agent_prompt = Opik_prompts.get_prompt(prompt_name=OpikPrompts.RESEARCH_AGENT_PROMPT)

    response = model_with_tools.invoke(
        [SystemMessage(content=research_agent_prompt)] + state[ConfigClass.RESEARCHER_MESSAGES]
    )
    return {
        ConfigClass.RESEARCHER_MESSAGES: [response]
    }


def tool_node(state: ResearcherState):

    tool_calls = state[ConfigClass.RESEARCHER_MESSAGES][-1].tool_calls

    observations = []
    for tool_call in tool_calls:
        tool = tools_by_name[tool_call["name"]]
        observations.append(tool.invoke(tool_call["args"]))
    
    tool_outputs = [
        ToolMessage(
            content=observation,
            name=tool_call["name"],
            tool_call_id=tool_call["id"]
        ) for observation, tool_call in zip(observations, tool_calls)
    ]
    state[ConfigClass.RESEARCHER_MESSAGES] = tool_outputs
    return state

def compress_research(state: ResearcherState):

    prompt = Opik_prompts.get_prompt(prompt_name=OpikPrompts.COMPRESS_RESEACH_SYSTEM_PROMPT)
    compress_research_human_prompt = Opik_prompts.get_prompt(prompt_name=OpikPrompts.COMPRESS_RESEACH_HUMAN_MESSAGE)
    compress_research_system_prompt = prompt.format(date=get_today_str())
    messages = [SystemMessage(content=compress_research_system_prompt)] + state.get(ConfigClass.RESEARCHER_MESSAGES, []) + [HumanMessage(content=compress_research_human_prompt)]

    response = compress_model.invoke(messages)

    raw_notes = [
        str(m.content) for m in filter_messages(
            state[ConfigClass.RESEARCHER_MESSAGES], 
            include_types=["tool", "ai"]
        )
    ]
    state[ConfigClass.COMPRESSED_RESEARCH] = str(response.content)
    state[ConfigClass.RAW_NOTES] = ["\n".join(raw_notes)]
    return state 

def should_continue(state: ResearcherState)->Literal[GraphNode]:

    messages = state[ConfigClass.RESEARCHER_MESSAGES]
    last_messages = messages[-1]

    if last_messages.tool_calls:
        return GraphNode.TOOL_NODE
    
    return GraphNode.COMPRESS_RESEARCH

def create_research_workflow():
    builder = StateGraph(ResearcherState, output_schema=ResearcherOutputState)

    builder.add_node(GraphNode.LLM_CALL, llm_call)
    builder.add_node(GraphNode.TOOL_NODE, tool_node)
    builder.add_node(GraphNode.COMPRESS_RESEARCH, compress_research)

    builder.add_edge(GraphNode.START, GraphNode.LLM_CALL)
    builder.add_conditional_edges(
    GraphNode.LLM_CALL,
    should_continue,
    {
        GraphNode.TOOL_NODE: GraphNode.TOOL_NODE,
        GraphNode.COMPRESS_RESEARCH: GraphNode.COMPRESS_RESEARCH,
    },
    )

    builder.add_edge(GraphNode.TOOL_NODE, GraphNode.LLM_CALL)
    builder.add_edge(GraphNode.COMPRESS_RESEARCH, GraphNode.END)

    return builder
    

research_agent = create_research_workflow().compile()