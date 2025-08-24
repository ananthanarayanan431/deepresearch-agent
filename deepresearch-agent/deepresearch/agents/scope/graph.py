import logging

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, get_buffer_string
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph
from langgraph.types import Command

from deepresearch.config.llm import LlmService
from deepresearch.core.constants import ConfigClass, GraphNode, OpikPrompts
from deepresearch.core.model import ClarifyWithUser, ResearchQuestion
from deepresearch.core.opik_prompts import Opik_prompts
from deepresearch.core.state import AgentInputState, AgentState
from deepresearch.tools.utils import get_today_str

load_dotenv()

llm = LlmService.get_model(model_name="gpt-4.1")
logger = logging.getLogger(__name__)


def clarify_with_user(state: AgentState) -> Command[GraphNode]:
    """Clarify with User"""

    structured_model = llm.with_structured_output(ClarifyWithUser)
    template = Opik_prompts.get_prompt(
        prompt_name=OpikPrompts.CLARIFY_WITH_USER_INSTRUCTIONS
    )
    prompt = template.format(
        messages=get_buffer_string(state[ConfigClass.MESSAGES]),
        date=get_today_str(),
    )
    logger.info(prompt)

    response = structured_model.invoke([HumanMessage(content=prompt)])

    if response.need_clarification:
        return Command(
            goto=GraphNode.END,
            update={ConfigClass.MESSAGES: [AIMessage(content=response.question)]},
        )
    else:
        return Command(
            goto=GraphNode.WRITE_RESEARCH_BRIEF,
            update={ConfigClass.MESSAGES: [AIMessage(content=response.verification)]},
        )


def write_research_brief(state: AgentState) -> AgentState:
    """writing the research brief"""

    structured_output_model = llm.with_structured_output(ResearchQuestion)
    prompt = Opik_prompts.get_prompt(
        prompt_name=OpikPrompts.TRANSFORM_MESSAGES_INTO_RESEARCH_TOPIC_PROMPT
    )
    template = prompt.format(
        messages=get_buffer_string(state[ConfigClass.MESSAGES]),
        date=get_today_str(),
    )

    response = structured_output_model.invoke([HumanMessage(content=template)])

    state[ConfigClass.RESEARCH_BRIEF] = response.research_brief
    state[ConfigClass.SUPERVISOR_MESSAGES] = [
        HumanMessage(content=f"{response.research_brief}.")
    ]
    return state


scope_builder = StateGraph(AgentState, input_schema=AgentInputState)
checkpointer = InMemorySaver()

scope_builder.add_node(GraphNode.CLARIFY_WITH_USER, clarify_with_user)
scope_builder.add_node(GraphNode.WRITE_RESEARCH_BRIEF, write_research_brief)

scope_builder.add_edge(GraphNode.START, GraphNode.CLARIFY_WITH_USER)
scope_builder.add_edge(GraphNode.WRITE_RESEARCH_BRIEF, GraphNode.END)

scope_graph = scope_builder.compile(checkpointer=checkpointer)
