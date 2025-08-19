# imports
from .profile_tool import Profile
from .research_tool import ResearchToolOutput

from pydantic import BaseModel, Field, AnyUrl
from typing import Optional, List, Annotated, Any, Dict
from langchain_core.output_parsers import StrOutputParser

from ..prompts.content_prompts import *
# from ..llm import llm  # assuming you have an llm object somewhere

# tools
class ContentTool:
    name = "content"
    description = "Generate LinkedIn content from profile and research analysis."

    '''
    Content creation tool for LinkedIn posts.

    This tool uses the user's profile and research data to generate relevant content.
    '''

    def __init__(self, llm):
        self.llm = llm

    async def run(self, **kwargs) -> Dict[str, Any]:
        '''
        Run the content creation tool.

        Args in kwargs:
            profile: Profile dict
            analysis: Research analysis dict

        Returns :
            dict: {
                "selected_trend": ...,
                "content": ...
            }
        '''
        profile = kwargs["profile"]
        analysis = kwargs["analysis"]

        # Step 1: Finalize the trend based on profile and analysis
        trend_chain = trend_finalize_prompt() | self.llm | StrOutputParser()
        best_trend = await trend_chain.ainvoke({'profile': profile, 'analysis': analysis})

        # Step 2: Use the finalized trend for content creation
        content_chain = content_creation_prompt() | self.llm | StrOutputParser()
        content = await content_chain.ainvoke({'trend': best_trend, 'analysis': analysis})

        return {
            'selected_trend': best_trend,
            'content': content
        }
