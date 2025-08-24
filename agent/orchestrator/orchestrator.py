# agent/orchestrator_dynamic.py
from __future__ import annotations
import asyncio
import logging
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional, Protocol, Tuple
from pydantic import BaseModel, Field, ValidationError

logger = logging.getLogger("linkedin_dynamic_agent")


# -------------------------
# Domain Models (Pydantic)
# -------------------------
# class Profile(BaseModel):
#     user_id: str
#     name: str
#     headline: Optional[str] = None
#     skills: List[str] = Field(default_factory=list)
#     raw: Dict[str, Any] = Field(default_factory=dict)


class Trend(BaseModel):
    title: str
    summary: Optional[str] = None
    source: Optional[str] = None
    url: Optional[str] = None


# class Post(BaseModel):
#     id: Optional[str] = None
#     user_id: str
#     text: str
#     created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
#     scheduled_for: Optional[datetime] = None
#     metadata: Dict[str, Any] = Field(default_factory=dict)


class Analytics(BaseModel):
    post_id: str
    likes: int = 0
    comments: int = 0
    shares: int = 0
    impressions: Optional[int] = None
    fetched_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


# -------------------------
# Tool Protocols
# -------------------------
class ToolProtocol(Protocol):
    name: str
    description: str

    async def run(self, **kwargs) -> Dict[str, Any]:
        """
        Run the tool and return a JSON-serializable result.
        Each tool should accept keyword args only (for flexibility).
        """
        ...


# -------------------------
# LLM Mediator Protocol
# -------------------------
class ActionInstruction(BaseModel):
    """
    This is the schema the LLM MUST output (as JSON). The orchestrator will parse and validate it.
    Example:
    {
      "action": "call_tool",
      "tool": "research",
      "args": {"industry_keywords": ["ml", "nlp"], "limit": 3}
    }
    or
    {
      "action": "done",
      "reason": "post scheduled"
    }
    """
    action: str  # "call_tool" or "done"
    tool: Optional[str] = None
    args: Dict[str, Any] = Field(default_factory=dict)
    reason: Optional[str] = None


class LLMMediatorInterface(Protocol):
    async def decide(self, context: Dict[str, Any], available_tools: List[Dict[str, Any]]) -> ActionInstruction:
        """
        Given a context (profile, trace so far, etc.) and metadata about available tools,
        return an ActionInstruction object.
        """
        ...


# -------------------------
# Orchestrator (dynamic)
# -------------------------
class DynamicAgentOrchestrator:
    def __init__(self, mediator: LLMMediatorInterface, tool_registry: Dict[str, ToolProtocol], max_steps: int = 8):
        self.mediator = mediator
        self.tool_registry = tool_registry
        self.max_steps = max_steps

    async def run(self, user_id: int, initial_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Run the agent loop. The mediator will decide which tool to call next based on context and tool metadata.
        Returns a trace with the sequence of steps and any outputs.
        """
        logger.info("Starting dynamic agent for user_id=%s", user_id)
        trace: List[Dict[str, Any]] = []
        step = 0

        # Base context (the mediator and tools will use this)
        context: Dict[str, Any] = initial_context.copy() if initial_context else {}
        context.setdefault("user_id", user_id)
        context.setdefault("profile", None)
        context.setdefault("tools_called", [])

        # Build tool metadata list for mediator (name + description + input schema hint)
        available_tools_meta = [
            {"name": tname, "description": getattr(tool, "description", "")} for tname, tool in self.tool_registry.items()
        ]

        while step < self.max_steps:
            step += 1
            logger.info("Agent step %d/%d", step, self.max_steps)
            try:
                instruction = await self.mediator.decide(context=context, available_tools=available_tools_meta)
            except Exception as e:
                logger.exception("Mediator failed to decide: %s", e)
                trace.append({"step": step, "error": f"mediator_exception: {e}"})
                break

            # Validate instruction (should already be validated by mediator, but double-check)
            if not isinstance(instruction, ActionInstruction):
                try:
                    instruction = ActionInstruction.model_validate(instruction)
                except ValidationError as ve: 
                    logger.error("Invalid instruction returned by mediator: %s", ve)
                    trace.append({"step": step, "error": f"invalid_instruction: {ve}"})
                    break

            logger.info("Mediator instruction: %s", instruction.model_dump_json())
            if instruction.action == "done":
                trace.append({"step": step, "action": "done", "reason": instruction.reason})
                logger.info("Agent finished: %s", instruction.reason)
                break

            if instruction.action != "call_tool" or not instruction.tool:
                trace.append({"step": step, "error": "unsupported_action_or_missing_tool"})
                logger.error("Unsupported action or missing tool in instruction.")
                break

            tool_name = instruction.tool
            if tool_name not in self.tool_registry:
                trace.append({"step": step, "error": f"unknown_tool:{tool_name}"})
                logger.error("Unknown tool requested: %s", tool_name)
                break

            tool = self.tool_registry[tool_name]
            # Record in context who was called
            context["tools_called"].append({"tool": tool_name, "args": instruction.args, "timestamp": datetime.now(timezone.utc).isoformat()})

            # Run the tool (support arun/run; with timeout & error handling)
            try:
                if hasattr(tool, "arun"):
                    tool_result = await asyncio.wait_for(tool.arun(**instruction.args), timeout=30)
                else:
                    tool_result = await asyncio.wait_for(tool.run(**instruction.args), timeout=30)
                trace_entry = {"step": step, "tool": tool_name, "args": instruction.args, "result": tool_result}
                trace.append(trace_entry)
                # Merge tool_result into context for next decision
                context.setdefault("tool_outputs", []).append({tool_name: tool_result})
                # Optionally: collapse some outputs into top-level fields for ease
                if tool_name == "profile" and isinstance(tool_result, dict):
                    context["profile"] = tool_result.get("profile") or tool_result
                # Collect analyses if present
                if isinstance(tool_result, dict) and "analysis" in tool_result:
                    context.setdefault("analyses", {})[tool_name] = tool_result["analysis"]
            except asyncio.TimeoutError:
                logger.error("Tool %s timed out", tool_name)
                trace.append({"step": step, "tool": tool_name, "error": "timeout"})
            except Exception as e:
                logger.exception("Tool %s raised exception: %s", tool_name, e)
                trace.append({"step": step, "tool": tool_name, "error": str(e)})

        else:
            # If loop completes without break
            logger.warning("Max steps reached without 'done' action.")
            trace.append({"step": step, "error": "max_steps_reached"})

        result = {"user_id": user_id, "trace": trace, "finished_at": datetime.now(timezone.utc).isoformat()}
        logger.info("Agent run completed for user_id=%s", user_id)
        return result


# -------------------------
# Example: Rule-based mediator (fallback for dev/testing)
# -------------------------
class RuleBasedMediator:
    """
    Very simple mediator that decides a small fixed sequence:
      1) call profile
      2) call research
      3) call content
      4) call scheduler (or done)
    This exists so you can test the dynamic orchestrator without wiring an LLM.
    """
    def __init__(self, auto_publish: bool = False):
        self.auto_publish = auto_publish
        self._steps = 0

    async def decide(self, context: Dict[str, Any], available_tools: List[Dict[str, Any]]) -> ActionInstruction:
        self._steps += 1
        # Step 1: if no profile yet -> fetch it
        if context.get("profile") is None:
            return ActionInstruction(action="call_tool", tool="profile", args={"user_id": context["user_id"]})
        # Step 2: if no trends -> research
        if not any("research" in out for out in context.get("tool_outputs", [])):
            # pass top keywords if profile available
            keywords = context["profile"].get("skills", [])[:3] if isinstance(context["profile"], dict) else []
            return ActionInstruction(action="call_tool", tool="research", args={"industry_keywords": keywords, "limit": 3})
        # Step 3: generate content
        if not any("content" in out for out in context.get("tool_outputs", [])):
            return ActionInstruction(action="call_tool", tool="content", args={"instruction": "Create a 3-5 sentence LinkedIn post.", "profile": context["profile"]})
        # Step 4: schedule or publish
        if not any("scheduler" in out for out in context.get("tool_outputs", [])):
            if self.auto_publish:
                return ActionInstruction(action="call_tool", tool="scheduler", args={"publish_now": True})
            return ActionInstruction(action="call_tool", tool="scheduler", args={"publish_now": False, "schedule_time": None})
        # Done
        return ActionInstruction(action="done", reason="All core tasks completed.")


# -------------------------
# Dummy Tool Implementations (for local testing)
# -------------------------
class DummyProfileTool:
    name = "profile"
    description = "Fetch and analyze LinkedIn profile for a user."

    async def run(self, user_id: str) -> Dict[str, Any]:
        # Simulate an API call
        await asyncio.sleep(0.1)
        profile = Profile(user_id=user_id, name="Aditya Rawat", headline="ML Engineer", skills=["ML", "NLP", "Python"], raw={"mocked": True})
        return profile.model_dump()  # Pydantic -> dict


class DummyResearchTool:
    name = "research"
    description = "Fetch the top trending topics given keywords."

    async def run(self, industry_keywords: List[str], limit: int = 3) -> Dict[str, Any]:
        await asyncio.sleep(0.1)
        trends = [Trend(title=f"Trend: {kw}", summary="Short summary", source="NewsAPI").model_dump() for kw in industry_keywords[:limit] or ["ai", "ml", "nlp"]]
        return {"trends": trends}


class DummyContentTool:
    name = "content"
    description = "Generate a LinkedIn post text using LLM."

    async def run(self, profile: Dict[str, Any], instruction: str = "") -> Dict[str, Any]:
        await asyncio.sleep(0.1)
        pname = profile.get("name", "User")
        trends = profile.get("skills", [])[:2]
        text = f"{pname}: Sharing thoughts on {', '.join(trends)}. {instruction}"
        post = Post(id=None, user_id=profile["user_id"], text=text)
        return post.model_dump()


class DummySchedulerTool:
    name = "scheduler"
    description = "Schedule or publish a post to LinkedIn."

    async def run(self, publish_now: bool = False, schedule_time: Optional[str] = None) -> Dict[str, Any]:
        await asyncio.sleep(0.1)
        if publish_now:
            # simulate publish
            return {"published": True, "post_id": "linkedin-post-123"}
        # else schedule -> return scheduled id/info
        return {"scheduled": True, "scheduled_for": schedule_time or "tomorrow 9AM"}


# -------------------------
# Quick demo usage
# -------------------------
async def _demo():
    # Register tools
    tools = {
        "profile": DummyProfileTool(),
        "research": DummyResearchTool(),
        "content": DummyContentTool(),
        "scheduler": DummySchedulerTool(),
    }

    mediator = RuleBasedMediator(auto_publish=False)
    orchestrator = DynamicAgentOrchestrator(mediator=mediator, tool_registry=tools, max_steps=8)

    result = await orchestrator.run(user_id="user-123", initial_context={})
    import json, pprint
    pprint.pprint(result)


if __name__ == "__main__":
    asyncio.run(_demo())

# Example: Running the agent with real tools (commented out)
# from .tool_registry import load_real_tools
#
# async def run_real_agent():
#     tools = load_real_tools()
#     agent = OrchestratorAgent(tools=tools)
#     # Example input, replace with real data
#     input_data = {
#         "profile_url": "https://www.linkedin.com/in/example/",
#         "post_content": "Excited to share my new project!",
#         # ...other fields as needed...
#     }
#     result = await agent.run(input_data)
#     print(result)
#
# # To run:
# # import asyncio
# # asyncio.run(run_real_agent())
