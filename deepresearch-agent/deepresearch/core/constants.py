from enum import Enum as PyEnum

from langgraph.graph import END, START


class GraphNode(str, PyEnum):
    START = START
    END = END
    CLARIFY_WITH_USER = "clarify_with_user"
    WRITE_RESEARCH_BRIEF = "write_research_brief"
    LLM_CALL = "llm_call"
    TOOL_NODE = "tool_node"
    COMPRESS_RESEARCH = "compress_research"
    SUPERVISOR_TOOLS = "supervisor_tools"
    SUPERVISOR = "supervisor"
    RESEARCH_COMPLETE = "ResearchComplete"
    CONDUCT_RESEARCH = "ConductResearch"
    THINK_TOOL = "think_tool"
    COMPRESSED_RESEARCH_GRAPH = "compressed_research"
    SUPERVISOR_SUBGRAPH = "supervisor_subgraph"
    FINAL_REPORT_GENERATION = "final_report_generation"


class ConfigClass(str, PyEnum):
    MESSAGES = "messages"
    RESEARCH_BRIEF = "research_brief"
    SUPERVISOR_MESSAGES = "supervisor_messages"
    RAW_NOTES = "raw_notes"
    NOTES = "notes"
    FINAL_REPORT = "final_report"
    RESEARCHER_MESSAGES = "researcher_messages"
    TOOL_CALL_INTERATIONS = "tool_call_iterations"
    RESEARCH_TOPIC = "research_topic"
    COMPRESSED_RESEARCH = "compressed_research"
    RESEARCH_ITERATIONS = "research_iterations"


class OpikPrompts(PyEnum):
    CLARIFY_WITH_USER_INSTRUCTIONS = "clarify_with_user_instructions"
    TRANSFORM_MESSAGES_INTO_RESEARCH_TOPIC_PROMPT = (
        "transform_messages_into_research_topic_prompt"
    )
    RESEARCH_AGENT_PROMPT = "research_agent_prompt"
    SUMMARIZE_WEBPAGE_PROMPT = "summarize_webpage_prompt"
    RESEARCH_AGENT_PROMPT_WITH_MCP = "research_agent_prompt_with_mcp"  # NOT USING
    LEAD_RESEARCHER_PROMPT = "lead_researcher_prompt"
    COMPRESS_RESEACH_SYSTEM_PROMPT = "compress_research_system_prompt"
    COMPRESS_RESEACH_HUMAN_MESSAGE = "compress_research_human_message"
    FINAL_REPORT_GENERTATION_PROMPT = "final_report_generation_prompt"
