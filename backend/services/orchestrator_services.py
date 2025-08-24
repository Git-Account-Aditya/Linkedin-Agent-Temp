from pydantic import BaseModel, ValidationError
from typing import Any, Dict, List
from langchain_core.tools import Tool
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import logging

from agent.orchestrator.orchestrator import ActionInstruction, DynamicAgentOrchestrator


logger = logging.getLogger("linkedin_dynamic_agent")


class OriginalLLMMediator:
    def __init__(self, context : Dict[str, Any], available_tools : List[Dict[str, Any]], llm: Any):
        self.context = context
        self.available_tools = available_tools
        self.llm = llm

    async def decide(self, context: Dict[str, Any], available_tools: List[Dict[str, Any]]) -> ActionInstruction:
        """
        Decide which action to take based on the context and available tools.
        
        :param query: The input query to process.
        :return: An ActionInstruction object containing the action to be taken.
        """
        # decision-making logic
        context = self.context
        available_tools = self.available_tools

        prompt = PromptTemplate(
            input_variables=["context", "tools"],
            template='''
                Given the context: {context} and available tools: {tools}, decide what next action should be taken 
                by agent.

                Return the structured output:
                This is the schema the LLM MUST output (as JSON). The orchestrator will parse and validate it.
                Example:
                {{
                "action": "call_tool",
                "tool": "research",
                "args": {{"industry_keywords": ["ml", "nlp"], "limit": 3}}
                }}
                or
                {{
                "action": "done",
                "reason": "post scheduled"
                }}
            '''
        )  

        chain = prompt | self.llm.with_structured_output(ActionInstruction)
        result = chain.invoke({"context": context, "tools": available_tools})

        # check if result is an ActionInstruction
        if isinstance(result, ActionInstruction):
            return result
        elif not isinstance(result, dict):
            try:
                result = ActionInstruction.model_validate(result)
            except ValidationError as ve:
                logger.error("Invalid instruction returned by mediator: %s", ve)
                raise TypeError("Expected ActionInstruction, got {}".format(type(result)))
        

async def run_agent(payload: dict):
    '''
        Payload should be like this:
            {
                "context": {
                    "user_id": 123,
                    "session_id": "abc"
                },
                "tools_available": [
                    {"name": "search", "type": "tool"},
                    {"name": "summarize", "type": "tool"}
                ],
                "llm": "ChatGroq(model='.....', api_key='.....')",
                "tools_registry": [
                    {"name": "search", "description": "Search the web"},
                    {"name": "summarize", "description": "Summarize text"}
                ]
            }
    '''
    context = payload.get("context", {})
    available_tools = payload.get("available_tools", [])
    llm = payload.get("llm", None)
    tool_registry = payload.get("tool_registry", [])

    orchestrator = DynamicAgentOrchestrator(
        mediator=OriginalLLMMediator(
            context=context,
            available_tools=available_tools,
            llm=llm()
        ),
        tool_registry=tool_registry,
        max_steps=12
    )

    response = await orchestrator.run(initial_context=context,
                                      user_id=context.get("user_id"))
    return response
