from typing import Annotated, Literal

from langchain_core.tools import InjectedToolArg, tool
from pydantic import BaseModel, Field

from deepresearch.agents.research.methods import (
    deduplicate_search_results,
    format_search_output,
    process_search_results,
)
from deepresearch.tools.tavilyapi import tavily_search_multiple
from deepresearch.tools.pplxapi import perplexity_client, perplexity_search_multiple


@tool(parse_docstring=True)
def tavily_search(
    query: str,
    max_results: Annotated[int, InjectedToolArg] = 3,
    topic: Annotated[
        Literal["general", "news", "finance"], InjectedToolArg
    ] = "general",
) -> str:
    """Fetch results from Tavily search API with content summarization.

    Args:
        query: A single search query to execute
        max_results: Maximum number of results to return
        topic: Topic to filter results by ('general', 'news', 'finance')

    Returns:
        Formatted string of search results with summaries
    """

    search_results = tavily_search_multiple(
        [query], max_results=max_results, topic=topic, include_raw_content=True
    )

    uniques_results = deduplicate_search_results(search_results)
    summarized_results = process_search_results(uniques_results)

    return format_search_output(summarized_results)


@tool
def think_tool(reflection: str) -> str:
    """Tool for strategic reflection on research progress and decision-making.

    Use this tool after each search to analyze results and plan next steps systematically.
    This creates a deliberate pause in the research workflow for quality decision-making.

    When to use:
    - After receiving search results: What key information did I find?
    - Before deciding next steps: Do I have enough to answer comprehensively?
    - When assessing research gaps: What specific information am I still missing?
    - Before concluding research: Can I provide a complete answer now?

    Reflection should address:
    1. Analysis of current findings - What concrete information have I gathered?
    2. Gap assessment - What crucial information is still missing?
    3. Quality evaluation - Do I have sufficient evidence/examples for a good answer?
    4. Strategic decision - Should I continue searching or provide my answer?

    Args:
        reflection: Your detailed reflection on research progress, findings, gaps, and next steps

    Returns:
        Confirmation that reflection was recorded for decision-making
    """
    return f"Reflection recorded: {reflection}"


@tool
class ConductResearch(BaseModel):
    """Tool for delegating a research task to a specialized sub-agent."""

    research_topic: str = Field(
        description="The topic to research. Should be a single topic, and should be described in high detail (at least a paragraph).",
    )


@tool
class ResearchComplete(BaseModel):
    """Tool for indicating that the research process is complete."""

    pass


@tool
def perplexity_search(
    query: str,
    max_results: Annotated[int, InjectedToolArg] = 3,
    search_mode: Annotated[
        Literal["web", "academic"], InjectedToolArg
    ] = "web",
    search_recency_filter: Annotated[
        Literal["day", "month"], InjectedToolArg
    ] = "month",
):
    """Searches the web content based on a given query and Fetch results. 
    from Perplexity Search API with Content Summarization
    
    Args:
        query (str): The search query.
        max_results (int): Maximum number of results to fetch.
        search_mode (str): Search mode ('web' or 'academic').
        search_recency_filter (str): Recency filter ('day' or 'month').

    Returns:
        List of search results.
    """
    
    search_results = perplexity_search_multiple(
        [query], max_results, search_mode, search_recency_filter
    )
    
    unique_results = ""
    return search_results
