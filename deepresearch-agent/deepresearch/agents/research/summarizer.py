from langchain_core.messages import HumanMessage

from deepresearch.config.llm import LlmService
from deepresearch.core.constants import StartEvaluationOpikPrompt
from deepresearch.core.model import Summary
from deepresearch.core.opik_prompts import Opik_prompts
from deepresearch.tools.utils import get_today_str

from deepresearch.config.gemini_models import GeminiModel

summarization_model = LlmService.get_gemini_model(model_name=GeminiModel.GEMINI_2_5_FLASH)


def summarize_webpage_content(webpage_content: str) -> str:
    """Summarize the webpage content"""

    try:
        structured_model = summarization_model.with_structured_output(Summary)
        prompt = Opik_prompts.get_prompt(
            prompt_name=StartEvaluationOpikPrompt.STARTUP_SUMMARIZE_WEBPAGE_PROMPT
        )
        template = prompt.format(webpage_content=webpage_content, date=get_today_str())

        summary = structured_model.invoke([HumanMessage(content=template)])
        formatted_summary = (
            f"<summary>\n{summary.summary}\n</summary>\n\n"
            f"<key_excerpts>\n{summary.key_excerpts}\n</key_excerpts>"
        )
        return formatted_summary
    except Exception as e:
        print(f"Failed to summarize webpage: {str(e)}")
        return (
            webpage_content[:1000] + "..."
            if len(webpage_content) > 1000
            else webpage_content
        )
