
from fastapi import FastAPI, HTTPException
from typing import Dict, Optional

from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import HumanMessage
from deepresearch.agents.writer.graph import deep_researcher_builder
from deepresearch.interface.schema import ChatRequest, ChatResponse
from deepresearch.core.constants import ConfigClass
from deepresearch.tools.utils import generate_session_id

RECURSION_LIMIT = 50

checkpointer = InMemorySaver()
full_agent = deep_researcher_builder.compile(checkpointer=checkpointer)
threads: Dict[str, Dict] = {}

app = FastAPI(title="DeepResearch Chatbot API", version="1.0")

@app.post("/chat")
async def chat_with_agent(request: ChatRequest)->ChatResponse:
    """Chat Interface"""

    try:
        thread_id = request.thread_id or generate_session_id()
        thread = threads.get(thread_id, {ConfigClass.CONFIGURABLE: {ConfigClass.THREAD_ID: thread_id, "recursion_limit": RECURSION_LIMIT}})

        reponse = await full_agent.ainvoke(
            {ConfigClass.MESSAGES: [HumanMessage(content=request.message)]},
            config=thread
        )

        final_report = reponse.get("final_report")
        response_text = reponse.get("response") or reponse.get("final_report", "Processing your request...")

        if final_report:
            new_thread_id = generate_session_id()
            threads[new_thread_id] = {ConfigClass.CONFIGURABLE: {ConfigClass.THREAD_ID: new_thread_id, "recursion_limit": RECURSION_LIMIT}}
            return ChatResponse(
                thread_id=new_thread_id,
                response=final_report,
                report=final_report,
                is_followup=False
            )
        else:
            # Clarification phase -> keep using same thread
            threads[thread_id] = thread
            return ChatResponse(
                thread_id=thread_id,
                response=response_text,
                is_followup=True
            )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


