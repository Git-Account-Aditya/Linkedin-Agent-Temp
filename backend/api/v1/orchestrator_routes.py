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


# call tools
def load_tools(linkedinapi, researchapi, llm):
    return [
        ProfileScrapTool(linkedin_api=linkedinapi, llm=llm),
        ResearchTool(research_api=researchapi, llm=llm),
        ContentTool(llm=llm),
        SchedulerTool(),
        TimerTool(),
        PublisherTool(linkedin_api=linkedinapi)
    ]


_tools = load_tools(linkedinapi, researchapi, llm)

tools = {tool.name: tool for tool in _tools}


# Create the payload
payload = {
    'context': {
        'user_id': '12345'
    },
    'tool_registry': tools,
    'llm': llm,
    'available_tools': [{'name': name, 'description': tool.description} for name, tool in tools.items()]
    }

router = APIRouter()


@router.post("/run")
async def run(payload: dict):
    response = await run_agent(payload)
    return {"message": "Agent is running...",
            "response": response}

