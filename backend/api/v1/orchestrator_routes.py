from fastapi import APIRouter

from agent.tools.profile_tool import ProfileScrapTool
from agent.tools.content_tool import ContentTool
from agent.tools.research_tool import ResearchTool
from agent.tools.scheduler_tool import SchedulerTool
from agent.tools.timer_tool import TimerTool
from agent.tools.publisher_tool import PublisherTool
from agent.tools.utils import humanize_timedelta, parse_datetime_like

from backend.services.orchestrator_services import run_agent

from backend.api.linkedin_api import linkedinapi
from backend.api.research_api import researchapi
from agent.llm import llm


router = APIRouter()

# Instantiate API clients
_linkedin_client = linkedinapi(api='fake_api')
_research_client = researchapi(api='fake_api')

# Build tool registry with correct dependency types
_tools = [
    ProfileScrapTool(linkedin_api=_linkedin_client, llm=llm),  # llm as factory (not currently used)
    ResearchTool(research_api=_research_client, llm=llm),      # expects llm factory
    ContentTool(llm=llm()),                                    # expects llm instance
    SchedulerTool(),
    TimerTool(),
    PublisherTool(linkedin_api=_linkedin_client),
]

tools = {tool.name: tool for tool in _tools}

available_tools = [{'name': name, 'description': getattr(tool, 'description', '')} for name, tool in tools.items()]

@router.post("/run")
async def run(request_body: dict):
    user_id = (request_body or {}).get('user_id') or None
    payload = {
        'context': {
            'user_id': user_id,
        },
        'tool_registry': tools,
        'llm': llm,
        'available_tools': available_tools,
    }
    response = await run_agent(payload)
    return {"message": "Agent is running...", "response": response}

