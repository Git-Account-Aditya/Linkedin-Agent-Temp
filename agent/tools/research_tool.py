# imports
from langchain_core.tools import BaseTool
from langchain_core.output_parsers import StrOutputParser

from pydantic import BaseModel, Field, AnyUrl, PrivateAttr
from typing import Optional, Dict, Any, List

# import research api
# ....

from ..prompts.research_prompts import research_trends_prompt

class Trend(BaseModel):
    title: str = Field(..., description='Title of the trend')
    summary: Optional[str] = Field(None, description="Brief summary of the trend")
    sources: Optional[dict[str, AnyUrl]] = Field(None, description="Sources of the trend information")


class TrendAnalysisSchema(BaseModel):
    """Schema for the analysis output."""
    future_growth_potential: str = Field(..., description="Analysis of future growth potential")
    high_engagement_accounts: str = Field(..., description="Analysis of high engagement accounts")
    potential_challenges_and_risks: str = Field(..., description="Analysis of potential challenges and risks")


class AnalysisSchema(BaseModel):
    """Schema for the structured analysis output."""
    trend: TrendAnalysisSchema = Field(..., description="Detailed analysis of the trend")


class ResearchToolInput(BaseModel):
    """Schema for the research tool input."""
    field: str = Field(..., description="The field of interest for trends, e.g., 'AI', 'Climate Change', 'Finance'")


class ResearchToolOutput(BaseModel):
    """Schema for the research tool output."""
    trends: list[Trend] = Field(..., description="List of fetched trends with title, summary, and sources")
    analysis: Dict[str, Any] = Field(..., description="Analysis containing key insights and sources")



class ResearchTool(BaseTool):
    """
    Dynamic-agent compatible research tool for fetching and analyzing trends.
    """

    name: str = "research"
    description: str = (
        "Fetches the latest trends in a specific field and analyzes them "
        "to extract key insights and sources."
    )
    args_schema: type[BaseModel] = ResearchToolInput
    return_schema: type[BaseModel] = ResearchToolOutput

    _research_api: Any = PrivateAttr()
    _llm: Any = PrivateAttr()

    def __init__(self, research_api, llm):
        super().__init__()
        self._research_api = research_api
        self._llm = llm

    async def arun(self, field: str) -> Dict[str, Any]:
        '''
        Args in kwargs:
            field: The field of interest for trends, e.g., 'AI', 'Climate Change', 'Finance'

        Returns :
            dict: {
                "trends": [...list of Trend objects...],
                "analysis": {...analysis details...}
        }
        '''
        # Step 1: Fetch trends using the research API (list of dicts)
        trends = await self._research_api.fetch_trends(field)

        # Step 2: Analyze the fetched trends using the LLM
        prompt = research_trends_prompt()
        trend_analysis_chain = prompt | self._llm().with_structured_output(AnalysisSchema)
        analysis = await trend_analysis_chain.ainvoke({"trends": trends})

        '''
        analysis = {
            "trend": {
                "future_growth_potential": "...",
                "high_engagement_accounts": "...",
                "potential_challenges_and_risks": "..."
            }
        }
        '''
        return {
            "trends": trends,
            "analysis": analysis.model_dump() if hasattr(analysis, "model_dump") else analysis
        }

    async def _run(self, field: str) -> Dict[str, Any]:
        raise NotImplementedError("Synchronous execution not supported — use async mode.")
