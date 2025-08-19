# backend/main.py
import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from backend.api.v1 import content_routes, orchestrator_routes, profile_routes, schedule_routes
from backend.services.orchestrator_services import run_agent
from agent.llm import llm
from agent.tools.profile_tool import ProfileScrapTool
from agent.tools.content_tool import ContentTool
from agent.tools.research_tool import ResearchTool
from agent.tools.scheduler_tool import SchedulerTool
from agent.tools.timer_tool import TimerTool
from agent.tools.publisher_tool import PublisherTool

from backend.api.linkedin_api import linkedinapi
from backend.api.research_api import researchapi

# Create FastAPI app
app = FastAPI(
    title="Dynamic LinkedIn Agent API",
    description="Backend for orchestrating AI tools dynamically",
    version="1.0.0"
)

# Include orchestrator routes
app.include_router(orchestrator_routes.router, prefix="/api/v1/orchestrator", tags=["Orchestrator"])
app.include_router(profile_routes.router, prefix="/api/v1/profile", tags=["Profile"])
app.include_router(content_routes.router, prefix="/api/v1/content", tags=["Content"])
app.include_router(schedule_routes.router, prefix="/api/v1/schedule", tags=["Schedule"])

@app.get("/")
async def root():
    return {"message": "Backend is running", "status": "OK"}


@app.get("/test-run")
async def test_run():
    """
    Quick endpoint to test the orchestrator without API keys.
    """
    # Create dummy tool instances with fake APIs
    fake_linkedin_api = linkedinapi(api='fake_api')  # replace with mock class if needed
    fake_research_api = researchapi(api='fake_api')  # replace with mock class if needed

    tools = {
        "profile": ProfileScrapTool(linkedin_api=fake_linkedin_api, llm=llm()),
        "research": ResearchTool(research_api=fake_research_api, llm=llm()),
        "content": ContentTool(llm=llm()),
        "scheduler": SchedulerTool(),
        "timer": TimerTool(),
        "publisher": PublisherTool(linkedin_api=fake_linkedin_api)
    }

    payload = {
        "context": {"user_id": "test_user"},
        "available_tools": [{'name': name,
                            'description': tool.description} for name, tool in tools.items()],
        "llm": llm,
        "tool_registry": tools
    }

    result = await run_agent(payload)
    return {"status": "success", "result": result}


if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
