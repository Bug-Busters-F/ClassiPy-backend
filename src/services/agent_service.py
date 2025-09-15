from smolagents import CodeAgent, ToolCallingAgent, DuckDuckGoSearchTool, LiteLLMModel, PythonInterpreterTool, tool
from typing import Optional
from dotenv import load_dotenv
import os
# Tools
from src.services.tools.visit_webpage import VisitWebpageTool
from src.services.tools.web_search import DuckDuckGoSearchTool


class AgentService:
    def __init__(self):
        load_dotenv()

        ollama_model = os.getenv("OLLAMA_MODEL")
        ollama_port = os.getenv("OLLAMA_API_PORT")
        model_id = f"ollama_chat/{ollama_model}"
        api_base = f"http://localhost:{ollama_port}"

        self.model = LiteLLMModel(
            model_id=model_id,
            api_base=api_base,
        )
        self.agent = ToolCallingAgent(
            tools=[VisitWebpageTool(), DuckDuckGoSearchTool()],
            model=self.model
        )

    def run(self, prompt: str):
        return self.agent.run(prompt)