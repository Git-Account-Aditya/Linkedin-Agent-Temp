from typing import Dict

from ..tools.profile_tool import ProfileScrapTool
from ..tools.content_tool import ContentTool
from ..tools.research_tool import ResearchTool
from ..tools.scheduler_tool import SchedulerTool
from ..tools.timer_tool import TimerTool
from ..tools.publisher_tool import PublisherTool
# from ..tools.analytics_tool import AnalysisTool


# Example: Dependency injection for real tools (commented out)
# from ..llm import llm
# from ..integrations.linkedin_api import linkedin_api
# from ..integrations.research_api import research_api

# def load_real_tools() -> Dict[str, object]:
#     tools = {}
#     tools["profile"] = ProfileScrapTool(linkedin_api=linkedin_api, llm=llm)
#     tools["content"] = ContentTool(llm=llm)
#     tools["research"] = ResearchTool(research_api=research_api, llm=llm)
#     tools["scheduler"] = SchedulerTool()
#     tools["timer"] = TimerTool()
#     tools["publisher"] = PublisherTool(linkedin_api=linkedin_api)
#     # tools["analytics"] = AnalyticsTool(...)  # When implemented
#     return tools

def load_tools() -> Dict[str, object]:
    tools = {}
    for tool_cls in [ProfileScrapTool, ContentTool, ResearchTool, SchedulerTool, TimerTool, PublisherTool]:
        instance = tool_cls()
        tools[instance.name] = instance
    return tools
