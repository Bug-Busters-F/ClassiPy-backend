from smolagents import CodeAgent, ToolCallingAgent, DuckDuckGoSearchTool, LiteLLMModel, PythonInterpreterTool, tool
from typing import Optional

from src.services.tools.visit_webpage import VisitWebpageTool
from src.services.tools.web_search import DuckDuckGoSearchTool

class AgentService:
    def __init__(self):
        self.model = LiteLLMModel(
            model_id="ollama_chat/qwen3:0.6b",
            api_base="http://localhost:11434",
        )
        self.agent = ToolCallingAgent(
            tools=[VisitWebpageTool(), DuckDuckGoSearchTool()],
            model=self.model
        )

    def run(self, prompt: str):
        return self.agent.run(prompt)