from typing import Dict

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from langchain_core.messages import HumanMessage
from langchain_core.messages import AIMessage
from langgraph.checkpoint.memory import InMemorySaver

from deepresearch.agents.writer.graph import deep_researcher_builder
from deepresearch.core.constants import ConfigClass
from deepresearch.interface.schema import ChatRequest, ChatResponse
from deepresearch.tools.utils import generate_session_id

RECURSION_LIMIT = 50

checkpointer = InMemorySaver()
full_agent = deep_researcher_builder.compile(checkpointer=checkpointer)
threads: Dict[str, Dict] = {}

app = FastAPI(title="DeepResearch Chatbot API", version="1.0")

# Enhanced CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:8080",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8080",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "*",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "DeepResearch Chatbot API is running", "status": "healthy"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "DeepResearch Chatbot"}


@app.options("/health")
async def options_health():
    """Handle preflight request for health endpoint"""
    return {"message": "OK"}


@app.options("/chat")
async def options_chat():
    """Handle preflight request for chat endpoint"""
    return {"message": "OK"}


@app.post("/chat")
async def chat_with_agent(request: ChatRequest) -> ChatResponse:
    """Chat Interface"""
    try:
        thread_id = request.thread_id or generate_session_id()
        thread = threads.get(
            thread_id,
            {
                ConfigClass.CONFIGURABLE: {
                    ConfigClass.THREAD_ID: thread_id,
                    "recursion_limit": RECURSION_LIMIT,
                }
            },
        )

        print(f"Processing message: {request.message}")  # Debug log
        print(f"Using thread_id: {thread_id}")  # Debug log

        response = await full_agent.ainvoke(
            {ConfigClass.MESSAGES: [HumanMessage(content=request.message)]},
            config=thread,
        )

        print(f"Agent response keys: {response.keys()}")  # Debug log

        # Check if we have a final report (research complete)
        final_report = response.get("final_report")
        
        # Extract the latest AI message from the messages array
        messages = response.get(ConfigClass.MESSAGES, [])
        latest_ai_message = None
        
        # Find the last AI message in the conversation
        for message in reversed(messages):
            if isinstance(message, AIMessage):
                latest_ai_message = message.content
                break
        
        # Determine response text
        if final_report:
            # Research is complete, return the final report
            response_text = final_report
        elif latest_ai_message:
            # Use the latest AI message content
            response_text = latest_ai_message
        else:
            # Fallback
            response_text = "I'm processing your request. Please wait..."

        print(f"Final response text: {response_text[:100]}...")  # Debug log (first 100 chars)

        if final_report:
            # Research complete - create new thread for next conversation
            new_thread_id = generate_session_id()
            threads[new_thread_id] = {
                ConfigClass.CONFIGURABLE: {
                    ConfigClass.THREAD_ID: new_thread_id,
                    "recursion_limit": RECURSION_LIMIT,
                }
            }
            return ChatResponse(
                thread_id=new_thread_id,
                response=final_report,
                report=final_report,
                is_followup=False,
            )
        else:
            # Clarification phase or intermediate step - keep using same thread
            threads[thread_id] = thread
            return ChatResponse(
                thread_id=thread_id, 
                response=response_text, 
                is_followup=True
            )

    except Exception as e:
        print(f"Error in chat_with_agent: {str(e)}")
        import traceback
        traceback.print_exc()  # Print full traceback for debugging
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/threads/{thread_id}")
async def get_thread_info(thread_id: str):
    """Get information about a specific thread"""
    thread = threads.get(thread_id)
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")

    return {
        "thread_id": thread_id,
        "exists": True,
        "config": thread.get(ConfigClass.CONFIGURABLE, {}),
    }


@app.delete("/threads/{thread_id}")
async def clear_thread(thread_id: str):
    """Clear/delete a specific thread"""
    if thread_id in threads:
        del threads[thread_id]
        return {"message": f"Thread {thread_id} cleared successfully"}
    else:
        raise HTTPException(status_code=404, detail="Thread not found")


@app.get("/threads")
async def list_threads():
    """List all active threads"""
    return {"active_threads": list(threads.keys()), "count": len(threads)}


# Add a simple test endpoint to verify CORS
@app.get("/test")
async def test_endpoint():
    """Simple test endpoint"""
    return {"message": "CORS test successful", "timestamp": "2024"}


# Add error handling middleware
@app.middleware("http")
async def add_cors_header(request, call_next):
    """Add CORS headers to all responses"""
    try:
        response = await call_next(request)
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = (
            "GET, POST, PUT, DELETE, OPTIONS"
        )
        response.headers["Access-Control-Allow-Headers"] = "*"
        return response
    except Exception as e:
        print(f"Middleware error: {str(e)}")
        raise e
