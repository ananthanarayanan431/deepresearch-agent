
import os 
import re
from this import s
import requests
from typing import Optional, List
from dotenv import load_dotenv

load_dotenv()

from perplexity import Perplexity

from deepresearch.config.env import PPLX_API_KEY

perplexity_client = Perplexity(api_key=PPLX_API_KEY)

def perplexity_search_multiple(
    search_queries: List[str],
    max_results: int = 3,
    search_mode: str = "web",
    search_recency_filter: str = "month",
):
    """Searches multiple queries using Perplexity AI API.
    
    Args:
        search_queries (List[str]): List of search queries.
        max_retries (int, optional): Maximum number of retries. Defaults to 3.
        search_mode (str, optional): Search mode. Defaults to "web".
        search_recency_filter (str, optional): Search recency filter. Defaults to "month".
    
    Returns:
        Tuple[str, List[str]]: Tuple containing the search results and citations.
    """
    
    if not PPLX_API_KEY:
        raise ValueError("PPLX_API_KEY is not set")
        
    search_docs = []
    
    for query in search_queries:
        result = perplexity_client.search.create(
            query=query,
            max_results=max_results,
            search_mode=search_mode,
            # search_recency_filter=search_recency_filter,
        )
        
        search_docs.append(result)
        
    return search_docs


val = perplexity_search_multiple(search_queries=["Agentic AI"])
print(val)