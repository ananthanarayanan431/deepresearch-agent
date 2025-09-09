from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph

from deepresearch.agents.scope.graph import clarify_with_user, write_research_brief
from deepresearch.agents.supervisor.graph import supervisor_agent
from deepresearch.config.llm import LlmService
from deepresearch.core.constants import ConfigClass, GraphNode
from deepresearch.core.constants import StartEvaluationOpikPrompt
from deepresearch.core.opik_prompts import Opik_prompts
from deepresearch.core.state import AgentInputState, AgentState
from deepresearch.tools.utils import get_today_str

from deepresearch.config.gemini_models import GeminiModel

writer_model = LlmService.get_gemini_model(model_name=GeminiModel.GEMINI_2_5_FLASH)


async def final_report_generation(state: AgentState):
    """Final report"""

    notes = state.get(ConfigClass.NOTES, [])
    findings = "\n".join(notes)

    final_report_generation_prompt = Opik_prompts.get_prompt(
        prompt_name=StartEvaluationOpikPrompt.STARTUP_FINAL_REPORT_GENERATION_PROMPT
    )

    final_report_prompt = final_report_generation_prompt.format(
        research_brief=state.get(ConfigClass.RESEARCH_BRIEF, ""),
        findings=findings,
        date=get_today_str(),
    )

    final_report = await writer_model.ainvoke(
        [HumanMessage(content=final_report_prompt)]
    )
    return {
        ConfigClass.FINAL_REPORT: final_report.content,
        ConfigClass.MESSAGES: ["Here is the final report: " + final_report.content],
    }


deep_researcher_builder = StateGraph(AgentState, input_schema=AgentInputState)

# Add workflow nodes
deep_researcher_builder.add_node(GraphNode.CLARIFY_WITH_USER, clarify_with_user)
deep_researcher_builder.add_node(GraphNode.WRITE_RESEARCH_BRIEF, write_research_brief)
deep_researcher_builder.add_node(GraphNode.SUPERVISOR_SUBGRAPH, supervisor_agent)
deep_researcher_builder.add_node(
    GraphNode.FINAL_REPORT_GENERATION, final_report_generation
)

# Add workflow edges
deep_researcher_builder.add_edge(GraphNode.START, GraphNode.CLARIFY_WITH_USER)
deep_researcher_builder.add_edge(
    GraphNode.WRITE_RESEARCH_BRIEF, GraphNode.SUPERVISOR_SUBGRAPH
)
deep_researcher_builder.add_edge(
    GraphNode.SUPERVISOR_SUBGRAPH, GraphNode.FINAL_REPORT_GENERATION
)
deep_researcher_builder.add_edge(GraphNode.FINAL_REPORT_GENERATION, GraphNode.END)

# Compile the full workflow
agent = deep_researcher_builder.compile()
